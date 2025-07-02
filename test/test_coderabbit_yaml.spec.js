const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

// Note: Using standard Node.js testing approach with js-yaml library
// This test suite validates CodeRabbit YAML configuration files

describe('CodeRabbit YAML Configuration Tests', () => {
  let sampleYamlPath;
  let validConfig;
  let invalidConfig;

  beforeEach(() => {
    // Setup test data
    sampleYamlPath = path.join(__dirname, '../.coderabbit.yaml');
    
    validConfig = {
      version: '1.0',
      language: 'en-US',
      reviews: {
        profile: 'chill',
        request_changes_workflow: false,
        high_level_summary: true,
        poem: true,
        review_status: true,
        collapse_ellipsis: true,
        auto_review: {
          enabled: true,
          drafts: false
        }
      },
      chat: {
        auto_reply: true
      }
    };

    invalidConfig = {
      // Missing required version field
      language: 'invalid-locale',
      reviews: {
        profile: 'invalid-profile'
      }
    };
  });

  afterEach(() => {
    // Cleanup any temporary files created during tests
    const tempFiles = [
      path.join(__dirname, 'temp-valid.yml'),
      path.join(__dirname, 'temp-invalid.yml'),
      path.join(__dirname, 'temp-test-config.yaml')
    ];
    
    tempFiles.forEach(file => {
      if (fs.existsSync(file)) {
        fs.unlinkSync(file);
      }
    });
  });

  describe('YAML File Parsing', () => {
    test('should successfully parse valid YAML configuration', () => {
      const yamlContent = yaml.dump(validConfig);
      const tempFile = path.join(__dirname, 'temp-valid.yml');
      
      fs.writeFileSync(tempFile, yamlContent);
      
      expect(() => {
        const content = fs.readFileSync(tempFile, 'utf8');
        const parsed = yaml.load(content);
        expect(parsed).toBeDefined();
        expect(parsed.version).toBe('1.0');
      }).not.toThrow();
    });

    test('should handle malformed YAML gracefully', () => {
      const malformedYaml = `
        version: 1.0
        reviews:
          profile: chill
        invalid: [unclosed array
      `;
      
      expect(() => {
        yaml.load(malformedYaml);
      }).toThrow();
    });

    test('should handle empty YAML file', () => {
      const emptyYaml = '';
      const result = yaml.load(emptyYaml);
      expect(result).toBeUndefined();
    });

    test('should handle YAML with only comments', () => {
      const commentOnlyYaml = `
        # This is a comment
        # Another comment
      `;
      const result = yaml.load(commentOnlyYaml);
      expect(result).toBeUndefined();
    });

    test('should parse actual CodeRabbit configuration file', () => {
      if (fs.existsSync(sampleYamlPath)) {
        const content = fs.readFileSync(sampleYamlPath, 'utf8');
        const parsed = yaml.load(content);
        
        expect(parsed).toBeDefined();
        expect(parsed.version).toBeDefined();
        expect(parsed.reviews).toBeDefined();
      }
    });
  });

  describe('Configuration Schema Validation', () => {
    test('should validate required version field', () => {
      const configWithoutVersion = { ...validConfig };
      delete configWithoutVersion.version;
      
      const isValid = validateCodeRabbitConfig(configWithoutVersion);
      expect(isValid.valid).toBe(false);
      expect(isValid.errors).toContain('version is required');
    });

    test('should validate language field format', () => {
      const configWithInvalidLanguage = {
        ...validConfig,
        language: 'invalid-format'
      };
      
      const isValid = validateCodeRabbitConfig(configWithInvalidLanguage);
      expect(isValid.valid).toBe(false);
      expect(isValid.errors.some(err => err.includes('language'))).toBe(true);
    });

    test('should validate reviews profile options', () => {
      const validProfiles = ['chill', 'assertive'];
      const invalidProfile = 'invalid-profile';
      
      const configWithInvalidProfile = {
        ...validConfig,
        reviews: {
          ...validConfig.reviews,
          profile: invalidProfile
        }
      };
      
      const isValid = validateCodeRabbitConfig(configWithInvalidProfile);
      expect(isValid.valid).toBe(false);
    });

    test('should validate boolean fields', () => {
      const configWithInvalidBoolean = {
        ...validConfig,
        reviews: {
          ...validConfig.reviews,
          request_changes_workflow: 'not-a-boolean'
        }
      };
      
      const isValid = validateCodeRabbitConfig(configWithInvalidBoolean);
      expect(isValid.valid).toBe(false);
    });

    test('should accept valid complete configuration', () => {
      const isValid = validateCodeRabbitConfig(validConfig);
      expect(isValid.valid).toBe(true);
      expect(isValid.errors).toHaveLength(0);
    });

    test('should validate nested auto_review configuration', () => {
      const configWithInvalidAutoReview = {
        ...validConfig,
        reviews: {
          ...validConfig.reviews,
          auto_review: {
            enabled: 'not-boolean',
            drafts: 123
          }
        }
      };
      
      const isValid = validateCodeRabbitConfig(configWithInvalidAutoReview);
      expect(isValid.valid).toBe(false);
      expect(isValid.errors.length).toBeGreaterThan(0);
    });

    test('should validate chat configuration', () => {
      const configWithInvalidChat = {
        ...validConfig,
        chat: {
          auto_reply: 'not-boolean'
        }
      };
      
      const isValid = validateCodeRabbitConfig(configWithInvalidChat);
      expect(isValid.valid).toBe(false);
    });
  });

  describe('Configuration File Operations', () => {
    test('should load configuration from file system', () => {
      const yamlContent = yaml.dump(validConfig);
      const tempFile = path.join(__dirname, 'temp-valid.yml');
      
      fs.writeFileSync(tempFile, yamlContent);
      
      const loadedConfig = loadCodeRabbitConfig(tempFile);
      expect(loadedConfig).toEqual(validConfig);
    });

    test('should handle missing configuration file', () => {
      const nonExistentFile = path.join(__dirname, 'non-existent.yml');
      
      expect(() => {
        loadCodeRabbitConfig(nonExistentFile);
      }).toThrow('Configuration file not found');
    });

    test('should save configuration to file system', () => {
      const tempFile = path.join(__dirname, 'temp-test-config.yaml');
      
      saveCodeRabbitConfig(tempFile, validConfig);
      
      expect(fs.existsSync(tempFile)).toBe(true);
      const loadedConfig = loadCodeRabbitConfig(tempFile);
      expect(loadedConfig).toEqual(validConfig);
    });

    test('should preserve YAML formatting when saving', () => {
      const tempFile = path.join(__dirname, 'temp-test-config.yaml');
      
      saveCodeRabbitConfig(tempFile, validConfig);
      
      const content = fs.readFileSync(tempFile, 'utf8');
      expect(content).toContain('version:');
      expect(content).toContain('reviews:');
      expect(content).toContain('auto_review:');
    });
  });

  describe('Configuration Merging and Defaults', () => {
    test('should merge with default configuration', () => {
      const partialConfig = {
        version: '1.0',
        reviews: {
          profile: 'assertive'
        }
      };

      const merged = mergeWithDefaults(partialConfig);
      
      expect(merged.version).toBe('1.0');
      expect(merged.reviews.profile).toBe('assertive');
      expect(merged.reviews.high_level_summary).toBeDefined(); // Should have default
    });

    test('should handle nested object merging', () => {
      const partialConfig = {
        version: '1.0',
        reviews: {
          auto_review: {
            enabled: false
          }
        }
      };

      const merged = mergeWithDefaults(partialConfig);
      
      expect(merged.reviews.auto_review.enabled).toBe(false);
      expect(merged.reviews.auto_review.drafts).toBeDefined(); // Should have default
    });

    test('should not mutate original configuration', () => {
      const originalConfig = {
        version: '1.0',
        reviews: { profile: 'chill' }
      };

      const configCopy = JSON.parse(JSON.stringify(originalConfig));
      const merged = mergeWithDefaults(originalConfig);
      
      expect(originalConfig).toEqual(configCopy);
    });

    test('should override defaults with provided values', () => {
      const customConfig = {
        version: '2.0',
        language: 'fr-FR',
        reviews: {
          profile: 'assertive',
          poem: false
        }
      };

      const merged = mergeWithDefaults(customConfig);
      
      expect(merged.version).toBe('2.0');
      expect(merged.language).toBe('fr-FR');
      expect(merged.reviews.profile).toBe('assertive');
      expect(merged.reviews.poem).toBe(false);
    });
  });

  describe('Edge Cases and Error Handling', () => {
    test('should handle null configuration gracefully', () => {
      expect(() => {
        validateCodeRabbitConfig(null);
      }).not.toThrow();
      
      const result = validateCodeRabbitConfig(null);
      expect(result.valid).toBe(false);
    });

    test('should handle undefined configuration gracefully', () => {
      expect(() => {
        validateCodeRabbitConfig(undefined);
      }).not.toThrow();
      
      const result = validateCodeRabbitConfig(undefined);
      expect(result.valid).toBe(false);
    });

    test('should handle configuration with extra unknown fields', () => {
      const configWithExtra = {
        ...validConfig,
        unknownField: 'should be ignored',
        nested: {
          unknownNested: 'should also be ignored'
        }
      };
      
      const result = validateCodeRabbitConfig(configWithExtra);
      expect(result.valid).toBe(true); // Should be tolerant of extra fields
    });

    test('should handle very large configuration files', () => {
      const largeConfig = {
        ...validConfig,
        large_array: new Array(1000).fill('test-data')
      };
      
      expect(() => {
        const yamlString = yaml.dump(largeConfig);
        const parsed = yaml.load(yamlString);
        validateCodeRabbitConfig(parsed);
      }).not.toThrow();
    });

    test('should handle configurations with special characters', () => {
      const configWithSpecialChars = {
        ...validConfig,
        special_field: 'Test with émojis 🚀 and ünïcödé characters'
      };
      
      const yamlString = yaml.dump(configWithSpecialChars);
      const parsed = yaml.load(yamlString);
      
      expect(parsed.special_field).toBe(configWithSpecialChars.special_field);
    });

    test('should handle circular references gracefully', () => {
      const circularConfig = { ...validConfig };
      circularConfig.self = circularConfig;
      
      expect(() => {
        yaml.dump(circularConfig);
      }).toThrow();
    });

    test('should handle deeply nested configurations', () => {
      const deepConfig = {
        version: '1.0',
        level1: {
          level2: {
            level3: {
              level4: {
                level5: {
                  value: 'deep'
                }
              }
            }
          }
        }
      };
      
      const yamlString = yaml.dump(deepConfig);
      const parsed = yaml.load(yamlString);
      
      expect(parsed.level1.level2.level3.level4.level5.value).toBe('deep');
    });
  });

  describe('Version Compatibility', () => {
    test('should handle different version formats', () => {
      const versionFormats = ['1.0', '1.0.0', '2.0', '2.1.3'];
      
      versionFormats.forEach(version => {
        const config = { ...validConfig, version };
        const result = validateCodeRabbitConfig(config);
        expect(result.valid).toBe(true);
      });
    });

    test('should reject invalid version formats', () => {
      const invalidVersions = ['v1.0', '1', 'latest', ''];
      
      invalidVersions.forEach(version => {
        const config = { ...validConfig, version };
        const result = validateCodeRabbitConfig(config);
        expect(result.valid).toBe(false);
      });
    });
  });

  describe('Profile Validation', () => {
    test('should accept all valid profile types', () => {
      const validProfiles = ['chill', 'assertive'];
      
      validProfiles.forEach(profile => {
        const config = {
          ...validConfig,
          reviews: { ...validConfig.reviews, profile }
        };
        const result = validateCodeRabbitConfig(config);
        expect(result.valid).toBe(true);
      });
    });

    test('should reject invalid profile types', () => {
      const invalidProfiles = ['aggressive', 'relaxed', 'custom', ''];
      
      invalidProfiles.forEach(profile => {
        const config = {
          ...validConfig,
          reviews: { ...validConfig.reviews, profile }
        };
        const result = validateCodeRabbitConfig(config);
        expect(result.valid).toBe(false);
      });
    });
  });
});

// Helper functions that would be imported from the main module
function validateCodeRabbitConfig(config) {
  if (!config) {
    return { valid: false, errors: ['Configuration is null or undefined'] };
  }

  const errors = [];
  
  // Validate version
  if (!config.version) {
    errors.push('version is required');
  } else if (!/^\d+\.\d+(\.\d+)?$/.test(config.version)) {
    errors.push('version must be in format X.Y or X.Y.Z');
  }

  // Validate language
  if (config.language && !/^[a-z]{2}-[A-Z]{2}$/.test(config.language)) {
    errors.push('language must be in format xx-XX (e.g., en-US)');
  }

  // Validate reviews section
  if (config.reviews) {
    if (config.reviews.profile) {
      const validProfiles = ['chill', 'assertive'];
      if (!validProfiles.includes(config.reviews.profile)) {
        errors.push(`reviews.profile must be one of: ${validProfiles.join(', ')}`);
      }
    }

    // Validate boolean fields
    const booleanFields = [
      'request_changes_workflow',
      'high_level_summary',
      'poem',
      'review_status',
      'collapse_ellipsis'
    ];

    booleanFields.forEach(field => {
      if (config.reviews[field] !== undefined && typeof config.reviews[field] !== 'boolean') {
        errors.push(`reviews.${field} must be a boolean`);
      }
    });

    // Validate auto_review section
    if (config.reviews.auto_review) {
      const autoReviewFields = ['enabled', 'drafts'];
      autoReviewFields.forEach(field => {
        if (config.reviews.auto_review[field] !== undefined && 
            typeof config.reviews.auto_review[field] !== 'boolean') {
          errors.push(`reviews.auto_review.${field} must be a boolean`);
        }
      });
    }
  }

  // Validate chat section
  if (config.chat) {
    if (config.chat.auto_reply !== undefined && typeof config.chat.auto_reply !== 'boolean') {
      errors.push('chat.auto_reply must be a boolean');
    }
  }

  return { valid: errors.length === 0, errors };
}

function loadCodeRabbitConfig(filePath) {
  if (!fs.existsSync(filePath)) {
    throw new Error('Configuration file not found');
  }

  try {
    const content = fs.readFileSync(filePath, 'utf8');
    return yaml.load(content);
  } catch (error) {
    throw new Error(`Failed to load configuration: ${error.message}`);
  }
}

function saveCodeRabbitConfig(filePath, config) {
  try {
    const yamlContent = yaml.dump(config, {
      indent: 2,
      lineWidth: -1,
      noRefs: true
    });
    fs.writeFileSync(filePath, yamlContent, 'utf8');
  } catch (error) {
    throw new Error(`Failed to save configuration: ${error.message}`);
  }
}

function mergeWithDefaults(config) {
  const defaults = {
    version: '1.0',
    language: 'en-US',
    reviews: {
      profile: 'chill',
      request_changes_workflow: false,
      high_level_summary: true,
      poem: true,
      review_status: true,
      collapse_ellipsis: true,
      auto_review: {
        enabled: true,
        drafts: false
      }
    },
    chat: {
      auto_reply: true
    }
  };

  return deepMerge(defaults, config);
}

function deepMerge(target, source) {
  const result = { ...target };
  
  for (const key in source) {
    if (source[key] && typeof source[key] === 'object' && !Array.isArray(source[key])) {
      result[key] = deepMerge(target[key] || {}, source[key]);
    } else {
      result[key] = source[key];
    }
  }
  
  return result;
}

function getNestedValue(obj, path) {
  return path.split('.').reduce((current, key) => {
    return current && current[key] !== undefined ? current[key] : undefined;
  }, obj);
}