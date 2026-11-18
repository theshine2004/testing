const path = require('path');

module.exports = {
  rootDir: '..',
  testEnvironment: 'node',
  extensionsToTreatAsEsm: ['.ts'],
  moduleDirectories: [
    'auth-service/node_modules',
    'node_modules'
  ],
  moduleNameMapper: {
    '^sequelize$': '<rootDir>/auth-service/node_modules/sequelize',
    '^express$': '<rootDir>/auth-service/node_modules/express',
    '^(\\.{1,2}/.*)\\.js$': '$1',
  },
  transform: {
    '^.+\\.tsx?$': [
      '<rootDir>/auth-service/node_modules/ts-jest',
      {
        useESM: true,
        diagnostics: false,
        tsconfig: {
          target: 'ES2022',
          module: 'ESNext',
          moduleResolution: 'node',
          isolatedModules: true,
          allowSyntheticDefaultImports: true,
          esModuleInterop: true,
          skipLibCheck: true,
          noImplicitAny: false,
          strict: false,
        },
      },
    ],
  },
  testMatch: ['<rootDir>/auth-service/src/__tests__/userController.editProfile.test.ts'],
  collectCoverageFrom: [
    '<rootDir>/user-service/src/services/userService.ts',
    '<rootDir>/user-service/src/controllers/userController.ts',
  ],
  coverageDirectory: '<rootDir>/Edit_Personal_Information_Unit_Testing/Coverage_Report',
  coverageReporters: ['text', 'text-summary', 'lcov', 'html'],
  verbose: true,
};
