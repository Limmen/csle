import React, { lazy, Suspense } from 'react';

const LazyMain = lazy(() => import('./DefenderDefaultPage'));

const Main = props => (
  <Suspense fallback={null}>
    <LazyMain {...props} />
  </Suspense>
);

export default Main;
