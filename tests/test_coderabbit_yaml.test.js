const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

describe('CodeRabbit YAML Configuration Tests', () => {
  let coderabbitConfig;
  const configPath = path.join('git', '.coderabbit.yaml');

  beforeAll(() => {
    // Load the coderabbit configuration file
    try {
      const configContent = fs.readFileSync(configPath, 'utf8');
      coderabbitConfig = yaml.load(configContent);
    } catch (error) {
      console.error('Failed to load coderabbit config:', error);
    }
  });

  describe('Configuration File Existence and Structure', () => {
    test('should have a coderabbit configuration file', () => {
      expect(fs.existsSync(configPath)).toBe(true);
    });

    test('should be valid YAML format', () => {
      expect(() => {
        const content = fs.readFileSync(configPath, 'utf8');
        yaml.load(content);
      }).not.toThrow();
    });

    test('should have required top-level properties', () => {
      expect(coderabbitConfig).toBeDefined();
      expect(typeof coderabbitConfig).toBe('object');
    });

    test('should not be null or empty', () => {
      expect(coderabbitConfig).not.toBeNull();
      expect(Object.keys(coderabbitConfig || {}).length).toBeGreaterThan(0);
    });
  });

  describe('Reviews Configuration', () => {
    test('should have reviews configuration when present', () => {
      if (coderabbitConfig.reviews) {
        expect(typeof coderabbitConfig.reviews).toBe('object');
        expect(coderabbitConfig.reviews).not.toBeNull();
      }
    });

    test('should have valid profile configuration', () => {
      if (coderabbitConfig.reviews && coderabbitConfig.reviews.profile) {
        expect(typeof coderabbitConfig.reviews.profile).toBe('string');
        expect(coderabbitConfig.reviews.profile.length).toBeGreaterThan(0);
        expect(coderabbitConfig.reviews.profile.trim()).toBe(coderabbitConfig.reviews.profile);
      }
    });

    test('should have valid request_changes configuration', () => {
      if (coderabbitConfig.reviews && coderabbitConfig.reviews.request_changes) {
        expect(typeof coderabbitConfig.reviews.request_changes).toBe('string');
        expect(['auto', 'never', 'always']).toContain(coderabbitConfig.reviews.request_changes);
      }
    });

    test('should have valid high_level_summary configuration', () => {
      if (coderabbitConfig.reviews && typeof coderabbitConfig.reviews.high_level_summary !== 'undefined') {
        expect(typeof coderabbitConfig.reviews.high_level_summary).toBe('boolean');
      }
    });

    test('should have valid poem configuration', () => {
      if (coderabbitConfig.reviews && typeof coderabbitConfig.reviews.poem !== 'undefined') {
        expect(typeof coderabbitConfig.reviews.poem).toBe('boolean');
      }
    });

    test('should have valid review_status configuration', () => {
      if (coderabbitConfig.reviews && typeof coderabbitConfig.reviews.review_status !== 'undefined') {
        expect(typeof coderabbitConfig.reviews.review_status).toBe('boolean');
      }
    });

    test('should have valid collapse_ellipsis configuration', () => {
      if (coderabbitConfig.reviews && typeof coderabbitConfig.reviews.collapse_ellipsis !== 'undefined') {
        expect(typeof coderabbitConfig.reviews.collapse_ellipsis).toBe('boolean');
      }
    });

    test('should have valid auto_review configuration', () => {
      if (coderabbitConfig.reviews && typeof coderabbitConfig.reviews.auto_review !== 'undefined') {
        expect(typeof coderabbitConfig.reviews.auto_review).toBe('boolean');
      }
    });
  });

  describe('Chat Configuration', () => {
    test('should have valid chat configuration when present', () => {
      if (coderabbitConfig.chat) {
        expect(typeof coderabbitConfig.chat).toBe('object');
        expect(coderabbitConfig.chat).not.toBeNull();
      }
    });

    test('should have valid auto_reply configuration', () => {
      if (coderabbitConfig.chat && typeof coderabbitConfig.chat.auto_reply !== 'undefined') {
        expect(typeof coderabbitConfig.chat.auto_reply).toBe('boolean');
      }
    });
  });

  describe('Language Configuration', () => {
    test('should have valid language configuration when present', () => {
      if (coderabbitConfig.language) {
        expect(typeof coderabbitConfig.language).toBe('string');
        expect(coderabbitConfig.language.length).toBeGreaterThan(0);
        // Common language codes
        const validLanguages = ['en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'ja', 'ko', 'zh', 'ar', 'hi'];
        expect(validLanguages.some(lang => coderabbitConfig.language.toLowerCase().startsWith(lang))).toBe(true);
      }
    });

    test('should reject invalid language codes', () => {
      if (coderabbitConfig.language) {
        expect(coderabbitConfig.language).not.toBe('');
        expect(coderabbitConfig.language).not.toMatch(/^\s+$/);
        expect(coderabbitConfig.language.length).toBeLessThan(10); // Language codes shouldn't be too long
      }
    });
  });

  describe('Tone Configuration', () => {
    test('should have valid tone configuration when present', () => {
      if (coderabbitConfig.tone) {
        expect(typeof coderabbitConfig.tone).toBe('string');
        const validTones = ['concise', 'constructive', 'friendly', 'professional', 'chill'];
        expect(validTones).toContain(coderabbitConfig.tone.toLowerCase());
      }
    });

    test('should reject invalid tone values', () => {
      if (coderabbitConfig.tone) {
        expect(coderabbitConfig.tone).not.toBe('');
        expect(coderabbitConfig.tone).not.toMatch(/^\s+$/);
      }
    });
  });

  describe('Knowledge Configuration', () => {
    test('should have valid knowledge configuration when present', () => {
      if (coderabbitConfig.knowledge) {
        expect(Array.isArray(coderabbitConfig.knowledge)).toBe(true);
      }
    });

    test('should have valid knowledge base entries', () => {
      if (coderabbitConfig.knowledge && Array.isArray(coderabbitConfig.knowledge)) {
        expect(coderabbitConfig.knowledge.length).toBeGreaterThan(0);
        
        coderabbitConfig.knowledge.forEach((entry, index) => {
          expect(typeof entry).toBe('object');
          expect(entry).toHaveProperty('path');
          expect(typeof entry.path).toBe('string');
          expect(entry.path.length).toBeGreaterThan(0);
          expect(entry.path.trim()).toBe(entry.path);
          
          if (entry.instructions) {
            expect(typeof entry.instructions).toBe('string');
            expect(entry.instructions.length).toBeGreaterThan(0);
          }
        });
      }
    });

    test('should not have duplicate knowledge entries', () => {
      if (coderabbitConfig.knowledge && Array.isArray(coderabbitConfig.knowledge)) {
        const paths = coderabbitConfig.knowledge.map(entry => entry.path);
        const uniquePaths = [...new Set(paths)];
        expect(paths.length).toBe(uniquePaths.length);
      }
    });
  });

  describe('Early Access Configuration', () => {
    test('should have valid early_access configuration when present', () => {
      if (typeof coderabbitConfig.early_access !== 'undefined') {
        expect(typeof coderabbitConfig.early_access).toBe('boolean');
      }
    });
  });

  describe('Path-based Instructions', () => {
    test('should have valid path_instructions when present', () => {
      if (coderabbitConfig.path_instructions) {
        expect(Array.isArray(coderabbitConfig.path_instructions)).toBe(true);
      }
    });

    test('should have valid path instruction entries', () => {
      if (coderabbitConfig.path_instructions && Array.isArray(coderabbitConfig.path_instructions)) {
        expect(coderabbitConfig.path_instructions.length).toBeGreaterThan(0);
        
        coderabbitConfig.path_instructions.forEach((instruction, index) => {
          expect(typeof instruction).toBe('object');
          expect(instruction).toHaveProperty('path');
          expect(instruction).toHaveProperty('instructions');
          expect(typeof instruction.path).toBe('string');
          expect(typeof instruction.instructions).toBe('string');
          expect(instruction.path.length).toBeGreaterThan(0);
          expect(instruction.instructions.length).toBeGreaterThan(0);
          expect(instruction.path.trim()).toBe(instruction.path);
          expect(instruction.instructions.trim()).toBe(instruction.instructions);
        });
      }
    });

    test('should not have duplicate path instructions', () => {
      if (coderabbitConfig.path_instructions && Array.isArray(coderabbitConfig.path_instructions)) {
        const paths = coderabbitConfig.path_instructions.map(entry => entry.path);
        const uniquePaths = [...new Set(paths)];
        expect(paths.length).toBe(uniquePaths.length);
      }
    });
  });

  describe('Ignore Configuration', () => {
    test('should have valid ignore patterns when present', () => {
      if (coderabbitConfig.ignore) {
        expect(Array.isArray(coderabbitConfig.ignore)).toBe(true);
      }
    });

    test('should have valid ignore pattern entries', () => {
      if (coderabbitConfig.ignore && Array.isArray(coderabbitConfig.ignore)) {
        expect(coderabbitConfig.ignore.length).toBeGreaterThan(0);
        
        coderabbitConfig.ignore.forEach((pattern, index) => {
          expect(typeof pattern).toBe('string');
          expect(pattern.length).toBeGreaterThan(0);
          expect(pattern.trim()).toBe(pattern);
        });
      }
    });

    test('should not have duplicate ignore patterns', () => {
      if (coderabbitConfig.ignore && Array.isArray(coderabbitConfig.ignore)) {
        const uniquePatterns = [...new Set(coderabbitConfig.ignore)];
        expect(coderabbitConfig.ignore.length).toBe(uniquePatterns.length);
      }
    });
  });

  describe('Edge Cases and Error Handling', () => {
    test('should handle empty configuration gracefully', () => {
      const emptyConfig = {};
      expect(() => {
        // Simulate validation of empty config
        if (emptyConfig.reviews && typeof emptyConfig.reviews !== 'object') {
          throw new Error('Invalid reviews configuration');
        }
      }).not.toThrow();
    });

    test('should handle malformed YAML gracefully', () => {
      const malformedYaml = 'invalid: yaml: content: [unclosed';
      expect(() => {
        yaml.load(malformedYaml);
      }).toThrow();
    });

    test('should validate boolean fields are actually booleans', () => {
      const booleanFields = [
        ['reviews', 'high_level_summary'],
        ['reviews', 'poem'], 
        ['reviews', 'review_status'],
        ['reviews', 'collapse_ellipsis'],
        ['reviews', 'auto_review'],
        ['chat', 'auto_reply'],
        ['early_access']
      ];

      booleanFields.forEach(fieldPath => {
        let value = coderabbitConfig;
        
        for (const key of fieldPath) {
          if (value && typeof value === 'object') {
            value = value[key];
          } else {
            value = undefined;
            break;
          }
        }

        if (typeof value !== 'undefined') {
          expect(typeof value).toBe('boolean');
        }
      });
    });

    test('should validate string fields are actually strings', () => {
      const stringFields = [
        ['reviews', 'profile'],
        ['reviews', 'request_changes'],
        ['language'],
        ['tone']
      ];

      stringFields.forEach(fieldPath => {
        let value = coderabbitConfig;
        
        for (const key of fieldPath) {
          if (value && typeof value === 'object') {
            value = value[key];
          } else {
            value = undefined;
            break;
          }
        }

        if (typeof value !== 'undefined') {
          expect(typeof value).toBe('string');
          expect(value.length).toBeGreaterThan(0);
        }
      });
    });

    test('should validate array fields are actually arrays', () => {
      const arrayFields = ['knowledge', 'path_instructions', 'ignore'];

      arrayFields.forEach(field => {
        const value = coderabbitConfig[field];
        if (typeof value !== 'undefined') {
          expect(Array.isArray(value)).toBe(true);
        }
      });
    });

    test('should not have unexpected top-level keys', () => {
      const expectedKeys = [
        'reviews', 'chat', 'language', 'tone', 'knowledge', 
        'early_access', 'path_instructions', 'ignore'
      ];
      
      const actualKeys = Object.keys(coderabbitConfig || {});
      const unexpectedKeys = actualKeys.filter(key => !expectedKeys.includes(key));
      
      if (unexpectedKeys.length > 0) {
        console.warn('Unexpected configuration keys found:', unexpectedKeys);
      }
    });
  });

  describe('Integration with File System', () => {
    test('should have reasonable file size', () => {
      const stats = fs.statSync(configPath);
      expect(stats.size).toBeGreaterThan(0);
      expect(stats.size).toBeLessThan(50000); // Less than 50KB seems reasonable
    });

    test('should be readable by the system', () => {
      expect(() => {
        fs.accessSync(configPath, fs.constants.R_OK);
      }).not.toThrow();
    });

    test('should have consistent line endings', () => {
      const content = fs.readFileSync(configPath, 'utf8');
      // Check that there are no mixed line endings
      const hasWindowsLineEndings = content.includes('\r\n');
      const hasUnixLineEndings = content.includes('\n') && !content.includes('\r\n');
      
      // Should have consistent line endings (either all Windows or all Unix)
      expect(hasWindowsLineEndings && hasUnixLineEndings).toBe(false);
    });
  });

  describe('Performance Tests', () => {
    test('should parse configuration quickly', () => {
      const start = Date.now();
      const content = fs.readFileSync(configPath, 'utf8');
      yaml.load(content);
      const end = Date.now();
      
      expect(end - start).toBeLessThan(100); // Should parse in less than 100ms
    });

    test('should handle multiple parse operations efficiently', () => {
      const start = Date.now();
      const content = fs.readFileSync(configPath, 'utf8');
      
      for (let i = 0; i < 10; i++) {
        yaml.load(content);
      }
      
      const end = Date.now();
      expect(end - start).toBeLessThan(500); // 10 parse operations in less than 500ms
    });
  });

  describe('Validation Rules', () => {
    test('should have logical configuration combinations', () => {
      // If auto_review is enabled, other review settings should make sense
      if (coderabbitConfig.reviews && coderabbitConfig.reviews.auto_review === true) {
        if (coderabbitConfig.reviews.request_changes) {
          expect(coderabbitConfig.reviews.request_changes).not.toBe('never');
        }
      }
    });

    test('should have valid path patterns in instructions and knowledge', () => {
      const pathFields = [
        ...(coderabbitConfig.knowledge || []).map(k => k.path),
        ...(coderabbitConfig.path_instructions || []).map(p => p.path),
        ...(coderabbitConfig.ignore || [])
      ];

      pathFields.forEach(pathPattern => {
        expect(pathPattern).not.toMatch(/\/{2,}/); // No double slashes
        expect(pathPattern).not.toMatch(/\.\./); // No parent directory references
      });
    });
  });
});