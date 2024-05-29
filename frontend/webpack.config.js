const path = require('path');

module.exports = {
  entry: {
    main: './src/index.js',
    upload_receipts: './src/upload_receipts/index.js',
    edit_receipts: './src/edit_receipts/index.js',
  },
  output: {
    path: path.resolve(__dirname, 'static/frontend'),
    filename: '[name].js',
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env', '@babel/preset-react'],
          },
        },
      },
    ],
  },
};
