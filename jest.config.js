module.exports = {
  testEnvironment: 'node',
  testMatch: ['**/__tests__/**/*.js', '!**/client/**/*.test.js'],
  collectCoverage: true,
  coverageDirectory: 'coverage',
  coverageReporters: ['text', 'lcov'],
  verbose: true,
  transform: {
    '^.+\.js$': 'babel-jest'
  },
  forceExit: true
};