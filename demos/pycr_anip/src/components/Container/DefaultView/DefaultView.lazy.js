import React, { lazy, Suspense } from 'react';

const LazyMain = lazy(() => import('./DefaultView'));

const Main = props => (
  <Suspense fallback={null}>
    <LazyMain {...props} />
  </Suspense>
);

export default Main;
