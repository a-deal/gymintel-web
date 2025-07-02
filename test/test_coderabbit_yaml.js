const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

// Jest testing framework - comprehensive unit tests for CodeRabbit YAML functionality
describe('CodeRabbit YAML Configuration Tests', () => {
  
  describe('YAML File Validation', () => {
    test('should parse valid YAML configuration', () => {
      const validYaml = `
language: javascript
reviews:
  enabled: true
  auto_approve: false
  max_files: 100
`;
      expect(() => yaml.load(validYaml)).not.toThrow();
      const parsed = yaml.load(validYaml);
      expect(parsed).toHaveProperty('language', 'javascript');
      expect(parsed.reviews).toHaveProperty('enabled', true);
    });

    test('should handle empty YAML file', () => {
      const emptyYaml = '';
      const parsed = yaml.load(emptyYaml);
      expect(parsed).toBeUndefined();
    });

    test('should throw error for invalid YAML syntax', () => {
      const invalidYaml = `
language: javascript
reviews:
  enabled: true
  - invalid indentation
`;
      expect(() => yaml.load(invalidYaml)).toThrow();
    });

    test('should handle YAML with comments', () => {
      const yamlWithComments = `
# Configuration for CodeRabbit
language: javascript # Primary language
reviews:
  enabled: true # Enable reviews
  auto_approve: false # Disable auto-approval
`;
      expect(() => yaml.load(yamlWithComments)).not.toThrow();
      const parsed = yaml.load(yamlWithComments);
      expect(parsed.language).toBe('javascript');
    });

    test('should handle malformed YAML with tabs', () => {
      const yamlWithTabs = "language: javascript\n\treviews:\n\t\tenabled: true";
      expect(() => yaml.load(yamlWithTabs)).not.toThrow();
    });

    test('should handle YAML with Unicode characters', () => {
      const unicodeYaml = `
language: javascript
description: "Test with émojis 🚀 and ümlauts"
reviews:
  enabled: true
`;
      const parsed = yaml.load(unicodeYaml);
      expect(parsed.description).toBe("Test with émojis 🚀 and ümlauts");
    });
  });

  describe('Configuration Schema Validation', () => {
    test('should validate required fields exist', () => {
      const config = {
        language: 'javascript',
        reviews: {
          enabled: true
        }
      };
      
      expect(config).toHaveProperty('language');
      expect(config).toHaveProperty('reviews');
      expect(config.reviews).toHaveProperty('enabled');
    });

    test('should handle missing optional fields gracefully', () => {
      const minimalConfig = {
        language: 'javascript'
      };
      
      expect(minimalConfig).toHaveProperty('language');
      expect(minimalConfig.reviews).toBeUndefined();
    });

    test('should validate language field is string', () => {
      const config = yaml.load('language: javascript');
      expect(typeof config.language).toBe('string');
    });

    test('should validate reviews.enabled is boolean', () => {
      const config = yaml.load(`
language: javascript
reviews:
  enabled: true
`);
      expect(typeof config.reviews.enabled).toBe('boolean');
    });

    test('should handle numeric values correctly', () => {
      const config = yaml.load(`
language: javascript
reviews:
  max_files: 100
  timeout: 30.5
`);
      expect(typeof config.reviews.max_files).toBe('number');
      expect(typeof config.reviews.timeout).toBe('number');
      expect(config.reviews.max_files).toBe(100);
      expect(config.reviews.timeout).toBe(30.5);
    });

    test('should validate supported languages enum', () => {
      const supportedLanguages = ['javascript', 'typescript', 'python', 'java', 'go', 'rust'];
      const config = yaml.load('language: typescript');
      expect(supportedLanguages).toContain(config.language);
    });

    test('should handle invalid language gracefully', () => {
      const config = yaml.load('language: invalid_language');
      expect(config.language).toBe('invalid_language');
      // In a real implementation, this would trigger validation errors
    });
  });

  describe('Edge Cases and Error Handling', () => {
    test('should handle very large YAML files', () => {
      const largeConfig = {
        language: 'javascript',
        reviews: {
          enabled: true,
          rules: Array.from({ length: 1000 }, (_, i) => ({ rule: `rule${i}` }))
        }
      };
      const yamlString = yaml.dump(largeConfig);
      expect(() => yaml.load(yamlString)).not.toThrow();
    });

    test('should handle special characters in strings', () => {
      const configWithSpecialChars = `
language: "javascript"
description: "Configuration with special chars: !@#$%^&*(){}[]|\\:;\"'<>,.?/~"
reviews:
  enabled: true
`;
      expect(() => yaml.load(configWithSpecialChars)).not.toThrow();
      const parsed = yaml.load(configWithSpecialChars);
      expect(parsed.description).toBe("Configuration with special chars: !@#$%^&*(){}[]|\\:;\"'<>,.?/~");
    });

    test('should handle multiline strings', () => {
      const multilineYaml = `
language: javascript
description: |
  This is a long description
  that spans multiple lines
  and should be preserved
reviews:
  enabled: true
`;
      const parsed = yaml.load(multilineYaml);
      expect(parsed.description).toContain('multiple lines');
      expect(parsed.description).toContain('\n');
    });

    test('should handle folded multiline strings', () => {
      const foldedYaml = `
language: javascript
description: >
  This is a folded string
  that will be joined
  into a single line
reviews:
  enabled: true
`;
      const parsed = yaml.load(foldedYaml);
      expect(parsed.description).toBe('This is a folded string that will be joined into a single line\n');
    });

    test('should handle arrays correctly', () => {
      const yamlWithArrays = `
language: javascript
supported_languages:
  - javascript
  - typescript
  - python
  - java
reviews:
  ignore_paths:
    - "*.log"
    - "dist/*"
    - "node_modules/*"
`;
      const parsed = yaml.load(yamlWithArrays);
      expect(Array.isArray(parsed.supported_languages)).toBe(true);
      expect(parsed.supported_languages).toHaveLength(4);
      expect(parsed.supported_languages).toContain('typescript');
      expect(Array.isArray(parsed.reviews.ignore_paths)).toBe(true);
      expect(parsed.reviews.ignore_paths).toContain('*.log');
    });

    test('should handle nested objects', () => {
      const nestedYaml = `
language: javascript
reviews:
  enabled: true
  settings:
    auto_approve: false
    notifications:
      email: true
      slack: 
        enabled: false
        channel: "#code-reviews"
    rules:
      complexity:
        max_cyclomatic: 10
        max_nesting: 4
`;
      const parsed = yaml.load(nestedYaml);
      expect(parsed.reviews.settings.notifications.slack.channel).toBe('#code-reviews');
      expect(parsed.reviews.settings.rules.complexity.max_cyclomatic).toBe(10);
    });

    test('should handle null and undefined values', () => {
      const yamlWithNulls = `
language: javascript
description: null
optional_field: ~
empty_field:
reviews:
  enabled: true
`;
      const parsed = yaml.load(yamlWithNulls);
      expect(parsed.description).toBeNull();
      expect(parsed.optional_field).toBeNull();
      expect(parsed.empty_field).toBeNull();
    });

    test('should preserve boolean values correctly', () => {
      const booleanYaml = `
string_true: "true"
string_false: "false"
boolean_true: true
boolean_false: false
string_yes: "yes"
boolean_yes: yes
string_no: "no"
boolean_no: no
`;
      const parsed = yaml.load(booleanYaml);
      expect(parsed.string_true).toBe('true');
      expect(parsed.string_false).toBe('false');
      expect(parsed.boolean_true).toBe(true);
      expect(parsed.boolean_false).toBe(false);
      expect(parsed.string_yes).toBe('yes');
      expect(parsed.boolean_yes).toBe(true);
      expect(parsed.string_no).toBe('no');
      expect(parsed.boolean_no).toBe(false);
    });

    test('should handle empty arrays and objects', () => {
      const emptyStructuresYaml = `
language: javascript
empty_array: []
empty_object: {}
nested_empty:
  array: []
  object: {}
`;
      const parsed = yaml.load(emptyStructuresYaml);
      expect(Array.isArray(parsed.empty_array)).toBe(true);
      expect(parsed.empty_array).toHaveLength(0);
      expect(typeof parsed.empty_object).toBe('object');
      expect(Object.keys(parsed.empty_object)).toHaveLength(0);
    });

    test('should handle mixed array types', () => {
      const mixedArrayYaml = `
mixed_array:
  - "string"
  - 42
  - true
  - null
  - { key: "value" }
  - [1, 2, 3]
`;
      const parsed = yaml.load(mixedArrayYaml);
      expect(parsed.mixed_array).toHaveLength(6);
      expect(parsed.mixed_array[0]).toBe('string');
      expect(parsed.mixed_array[1]).toBe(42);
      expect(parsed.mixed_array[2]).toBe(true);
      expect(parsed.mixed_array[3]).toBeNull();
      expect(typeof parsed.mixed_array[4]).toBe('object');
      expect(Array.isArray(parsed.mixed_array[5])).toBe(true);
    });
  });

  describe('YAML Serialization/Deserialization', () => {
    test('should round-trip serialize and deserialize correctly', () => {
      const originalConfig = {
        language: 'javascript',
        reviews: {
          enabled: true,
          auto_approve: false,
          max_files: 100,
          ignore_paths: ['*.log', 'dist/*'],
          settings: {
            complexity: {
              max_cyclomatic: 10
            }
          }
        }
      };
      
      const yamlString = yaml.dump(originalConfig);
      const parsed = yaml.load(yamlString);
      
      expect(parsed).toEqual(originalConfig);
    });

    test('should handle dump options correctly', () => {
      const config = {
        language: 'javascript',
        very_long_description: 'This is a very long description that should potentially be wrapped when dumped to YAML format'
      };
      
      const yamlString = yaml.dump(config, { lineWidth: 50 });
      expect(yamlString).toBeDefined();
      expect(typeof yamlString).toBe('string');
      
      const parsed = yaml.load(yamlString);
      expect(parsed).toEqual(config);
    });

    test('should handle different indentation options', () => {
      const config = {
        reviews: {
          settings: {
            nested: {
              value: true
            }
          }
        }
      };
      
      const yamlWith2Spaces = yaml.dump(config, { indent: 2 });
      const yamlWith4Spaces = yaml.dump(config, { indent: 4 });
      
      expect(yamlWith2Spaces).not.toBe(yamlWith4Spaces);
      expect(yaml.load(yamlWith2Spaces)).toEqual(config);
      expect(yaml.load(yamlWith4Spaces)).toEqual(config);
    });

    test('should handle safe dump to prevent code injection', () => {
      const dangerousObject = {
        toString: () => 'dangerous',
        valueOf: () => 'dangerous'
      };
      
      expect(() => yaml.dump(dangerousObject)).not.toThrow();
    });
  });

  describe('File Operations', () => {
    const testConfigPath = path.join(__dirname, 'test-config.yml');
    const testConfigDir = path.join(__dirname, 'test-configs');
    
    afterEach(() => {
      // Clean up test files
      if (fs.existsSync(testConfigPath)) {
        fs.unlinkSync(testConfigPath);
      }
      if (fs.existsSync(testConfigDir)) {
        fs.rmSync(testConfigDir, { recursive: true, force: true });
      }
    });

    test('should read YAML file from filesystem', () => {
      const testConfig = {
        language: 'javascript',
        reviews: { enabled: true }
      };
      
      fs.writeFileSync(testConfigPath, yaml.dump(testConfig));
      
      const fileContent = fs.readFileSync(testConfigPath, 'utf8');
      const parsed = yaml.load(fileContent);
      
      expect(parsed).toEqual(testConfig);
    });

    test('should handle file read errors gracefully', () => {
      const nonExistentPath = path.join(__dirname, 'non-existent.yml');
      
      expect(() => {
        fs.readFileSync(nonExistentPath, 'utf8');
      }).toThrow();
    });

    test('should write YAML to filesystem correctly', () => {
      const testConfig = {
        language: 'typescript',
        reviews: {
          enabled: false,
          auto_approve: true
        }
      };
      
      const yamlContent = yaml.dump(testConfig);
      fs.writeFileSync(testConfigPath, yamlContent);
      
      expect(fs.existsSync(testConfigPath)).toBe(true);
      
      const readContent = fs.readFileSync(testConfigPath, 'utf8');
      const parsed = yaml.load(readContent);
      
      expect(parsed).toEqual(testConfig);
    });

    test('should handle multiple config files in directory', () => {
      fs.mkdirSync(testConfigDir, { recursive: true });
      
      const configs = [
        { name: 'config1.yml', content: { language: 'javascript' } },
        { name: 'config2.yml', content: { language: 'typescript' } },
        { name: 'config3.yml', content: { language: 'python' } }
      ];
      
      configs.forEach(config => {
        const filePath = path.join(testConfigDir, config.name);
        fs.writeFileSync(filePath, yaml.dump(config.content));
      });
      
      const files = fs.readdirSync(testConfigDir);
      expect(files).toHaveLength(3);
      
      configs.forEach(config => {
        const filePath = path.join(testConfigDir, config.name);
        const content = fs.readFileSync(filePath, 'utf8');
        const parsed = yaml.load(content);
        expect(parsed).toEqual(config.content);
      });
    });

    test('should handle file permissions and access', () => {
      const testConfig = { language: 'javascript' };
      fs.writeFileSync(testConfigPath, yaml.dump(testConfig));
      
      const stats = fs.statSync(testConfigPath);
      expect(stats.isFile()).toBe(true);
      expect(stats.size).toBeGreaterThan(0);
    });
  });

  describe('Performance and Memory Tests', () => {
    test('should handle parsing within reasonable time limits', () => {
      const complexConfig = {
        language: 'javascript',
        reviews: {
          enabled: true,
          rules: Array.from({ length: 100 }, (_, i) => ({
            id: `rule-${i}`,
            name: `Rule ${i}`,
            enabled: i % 2 === 0,
            settings: {
              threshold: i * 10,
              tags: [`tag-${i}`, `category-${i % 5}`]
            }
          }))
        }
      };
      
      const startTime = process.hrtime();
      const yamlString = yaml.dump(complexConfig);
      const parsed = yaml.load(yamlString);
      const [seconds, nanoseconds] = process.hrtime(startTime);
      const milliseconds = seconds * 1000 + nanoseconds / 1000000;
      
      expect(milliseconds).toBeLessThan(1000); // Should complete within 1 second
      expect(parsed).toEqual(complexConfig);
    });

    test('should handle deeply nested objects', () => {
      const createNestedObject = (depth) => {
        let obj = { value: depth };
        for (let i = 0; i < depth; i++) {
          obj = { nested: obj };
        }
        return obj;
      };
      
      const deepConfig = createNestedObject(50);
      const yamlString = yaml.dump(deepConfig);
      const parsed = yaml.load(yamlString);
      
      expect(parsed).toEqual(deepConfig);
    });

    test('should handle large string values', () => {
      const largeString = 'x'.repeat(10000);
      const config = {
        language: 'javascript',
        large_description: largeString
      };
      
      const yamlString = yaml.dump(config);
      const parsed = yaml.load(yamlString);
      
      expect(parsed.large_description).toBe(largeString);
      expect(parsed.large_description).toHaveLength(10000);
    });
  });

  describe('Type Coercion and Data Types', () => {
    test('should handle different numeric formats', () => {
      const numericYaml = `
integer: 42
float: 3.14159
scientific: 1.23e-4
negative: -42
zero: 0
octal: 0o755
hex: 0xFF
binary: 0b1010
`;
      const parsed = yaml.load(numericYaml);
      
      expect(parsed.integer).toBe(42);
      expect(parsed.float).toBeCloseTo(3.14159);
      expect(parsed.scientific).toBeCloseTo(0.000123);
      expect(parsed.negative).toBe(-42);
      expect(parsed.zero).toBe(0);
      expect(parsed.octal).toBe(493); // 0o755 in decimal
      expect(parsed.hex).toBe(255); // 0xFF in decimal
      expect(parsed.binary).toBe(10); // 0b1010 in decimal
    });

    test('should handle date formats', () => {
      const dateYaml = `
iso_date: 2023-01-15
iso_datetime: 2023-01-15T10:30:00Z
iso_datetime_with_offset: 2023-01-15T10:30:00+05:00
`;
      const parsed = yaml.load(dateYaml);
      
      expect(parsed.iso_date).toBeInstanceOf(Date);
      expect(parsed.iso_datetime).toBeInstanceOf(Date);
      expect(parsed.iso_datetime_with_offset).toBeInstanceOf(Date);
    });

    test('should handle string escaping', () => {
      const escapedYaml = `
single_quotes: 'He said "Hello"'
double_quotes: "She said 'Hi'"
escaped_chars: "Line 1\\nLine 2\\tTabbed"
unicode_escape: "Unicode: \\u0048\\u0065\\u006C\\u006C\\u006F"
`;
      const parsed = yaml.load(escapedYaml);
      
      expect(parsed.single_quotes).toBe('He said "Hello"');
      expect(parsed.double_quotes).toBe("She said 'Hi'");
      expect(parsed.escaped_chars).toBe("Line 1\nLine 2\tTabbed");
      expect(parsed.unicode_escape).toBe("Unicode: Hello");
    });

    test('should handle anchors and aliases', () => {
      const anchorYaml = `
defaults: &defaults
  timeout: 30
  retries: 3

development:
  <<: *defaults
  debug: true

production:
  <<: *defaults
  debug: false
`;
      const parsed = yaml.load(anchorYaml);
      
      expect(parsed.development.timeout).toBe(30);
      expect(parsed.development.retries).toBe(3);
      expect(parsed.development.debug).toBe(true);
      expect(parsed.production.timeout).toBe(30);
      expect(parsed.production.retries).toBe(3);
      expect(parsed.production.debug).toBe(false);
    });

    test('should handle complex data structures', () => {
      const complexYaml = `
matrix:
  - [1, 2, 3]
  - [4, 5, 6]
  - [7, 8, 9]

nested_maps:
  level1:
    level2:
      level3: "deep value"
      array: [a, b, c]

mixed_types:
  string: "hello"
  number: 42
  boolean: true
  null_value: null
  array: [1, "two", true]
  object: { key: "value" }
`;
      const parsed = yaml.load(complexYaml);
      
      expect(parsed.matrix).toHaveLength(3);
      expect(parsed.matrix[0]).toEqual([1, 2, 3]);
      expect(parsed.nested_maps.level1.level2.level3).toBe("deep value");
      expect(parsed.mixed_types.array).toEqual([1, "two", true]);
    });
  });

  describe('Error Recovery and Validation', () => {
    test('should provide meaningful error messages for syntax errors', () => {
      const invalidYamls = [
        'invalid: yaml: content:',
        'key: value\n\tinvalid indentation',
        'unclosed: "string value',
        'duplicate:\n  key: value1\n  key: value2'
      ];
      
      invalidYamls.forEach(yamlString => {
        expect(() => yaml.load(yamlString)).toThrow();
      });
    });

    test('should handle partial YAML loading', () => {
      const partialYaml = `
language: javascript
reviews:
  enabled: true
# End of valid content
invalid content here that should be ignored if loading stops
`;
      
      // In real implementation, you might want to load only the valid portion
      expect(() => yaml.load(partialYaml)).toThrow();
    });

    test('should validate required schema fields', () => {
      const validateConfig = (config) => {
        const requiredFields = ['language'];
        const missingFields = requiredFields.filter(field => !(field in config));
        return missingFields.length === 0;
      };
      
      const validConfig = { language: 'javascript', reviews: { enabled: true } };
      const invalidConfig = { reviews: { enabled: true } };
      
      expect(validateConfig(validConfig)).toBe(true);
      expect(validateConfig(invalidConfig)).toBe(false);
    });

    test('should handle circular references in objects', () => {
      const circularObj = { language: 'javascript' };
      circularObj.self = circularObj;
      
      // yaml.dump should handle circular references gracefully or throw
      expect(() => yaml.dump(circularObj)).toThrow();
    });
  });

  describe('Integration and Real-world Scenarios', () => {
    test('should handle typical CodeRabbit configuration', () => {
      const coderabbitConfig = `
language: javascript
reviews:
  enabled: true
  auto_approve: false
  path_filters:
    - "src/**/*.js"
    - "src/**/*.ts"
    - "!src/**/*.test.js"
  rules:
    complexity:
      enabled: true
      max_cyclomatic: 10
    security:
      enabled: true
      check_dependencies: true
    style:
      enabled: false
notifications:
  slack:
    enabled: true
    webhook_url: "https://hooks.slack.com/services/..."
    channel: "#code-reviews"
  email:
    enabled: false
`;
      
      const parsed = yaml.load(coderabbitConfig);
      
      expect(parsed.language).toBe('javascript');
      expect(parsed.reviews.enabled).toBe(true);
      expect(parsed.reviews.path_filters).toContain('src/**/*.js');
      expect(parsed.reviews.path_filters).toContain('!src/**/*.test.js');
      expect(parsed.reviews.rules.complexity.max_cyclomatic).toBe(10);
      expect(parsed.notifications.slack.channel).toBe('#code-reviews');
    });

    test('should handle environment-specific configurations', () => {
      const envConfigs = {
        development: `
language: javascript
reviews:
  enabled: true
  auto_approve: true
debug: true
`,
        production: `
language: javascript
reviews:
  enabled: true
  auto_approve: false
debug: false
`
      };
      
      Object.entries(envConfigs).forEach(([env, config]) => {
        const parsed = yaml.load(config);
        expect(parsed.language).toBe('javascript');
        expect(parsed.reviews.enabled).toBe(true);
        expect(parsed.debug).toBe(env === 'development');
      });
    });

    test('should handle configuration merging', () => {
      const baseConfig = yaml.load(`
language: javascript
reviews:
  enabled: true
  rules:
    complexity:
      enabled: true
      max_cyclomatic: 10
`);
      
      const overrideConfig = yaml.load(`
reviews:
  auto_approve: true
  rules:
    complexity:
      max_cyclomatic: 15
    security:
      enabled: true
`);
      
      // Simple merge logic for demonstration
      const merged = {
        ...baseConfig,
        reviews: {
          ...baseConfig.reviews,
          ...overrideConfig.reviews,
          rules: {
            ...baseConfig.reviews.rules,
            ...overrideConfig.reviews.rules,
            complexity: {
              ...baseConfig.reviews.rules.complexity,
              ...overrideConfig.reviews.rules.complexity
            }
          }
        }
      };
      
      expect(merged.language).toBe('javascript');
      expect(merged.reviews.enabled).toBe(true);
      expect(merged.reviews.auto_approve).toBe(true);
      expect(merged.reviews.rules.complexity.max_cyclomatic).toBe(15);
      expect(merged.reviews.rules.security.enabled).toBe(true);
    });
  });
});