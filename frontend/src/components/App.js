import React, { Suspense, lazy } from 'react';

const MyComponent = lazy(() => import('./MyComponent'));

const App = () => {
  return (
    <div>
      <h1>Hello, React in Django!</h1>
      <Suspense fallback={<div>Loading...</div>}>
        <MyComponent />
      </Suspense>
    </div>
  );
};

export default App;
