import React, { Suspense, lazy } from 'react';
// lazyってなんだっけ
const Component1 = lazy(() => import('./Component1'));

const EditMock = () => {
  return (
    <div>
      <h1>Hello, React in Django!</h1>
      <Suspense fallback={<div>Loading...</div>}>
        <Component1 />
      </Suspense>
    </div>
  );
};

export default EditMock;
