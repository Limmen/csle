import React, { lazy, Suspense } from 'react';

const LazyMain = lazy(() => import('./Main'));

const Main = props => (
  <Suspense fallback={null}>
    <LazyMain {...props} />
  </Suspense>
);

export default Main;
