module.exports = {
  preset: 'ts-jest/presets/default-esm',
  testEnvironment: 'node',
  extensionsToTreatAsEsm: ['.ts'],
  moduleDirectories: ['node_modules', '<rootDir>/node_modules'],
  moduleNameMapper: {
    '^sequelize$': '<rootDir>/node_modules/sequelize',
    '^express$': '<rootDir>/node_modules/express',
    '^(\\.{1,2}/.*)\\.js$': '$1',
  },
  transform: {
    '^.+\\.tsx?$': [
      'ts-jest',
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
  testMatch: ['**/__tests__/**/*.test.ts'],
  collectCoverageFrom: [
    'src/controllers/authController.ts',
    'src/services/tokenService.ts',
  ],
  coverageDirectory: 'coverage',
  coverageReporters: ['text', 'text-summary', 'lcov', 'html'],
  verbose: true,
};
