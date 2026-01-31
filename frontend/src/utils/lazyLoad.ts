/**
 * Lazy Loading Utilities
 * =======================
 * Utilities for code splitting and lazy loading components.
 */

import { lazy } from 'react';
import type { ComponentType } from 'react';

/**
 * Retry lazy loading up to 3 times before failing
 * Helps with network issues and failed chunk loading
 */
export function lazyRetry<T extends ComponentType<any>>(
  componentImport: () => Promise<{ default: T }>,
  name: string,
  retriesLeft = 3,
  interval = 1000
): React.LazyExoticComponent<T> {
  return lazy(() =>
    componentImport().catch((error) => {
      // Retry logic
      if (retriesLeft === 0) {
        console.error(`Failed to load component "${name}" after 3 retries:`, error);
        throw error;
      }

      console.warn(`Retrying to load component "${name}"... (${3 - retriesLeft + 1}/3)`);

      return new Promise((resolve) => {
        setTimeout(() => {
          resolve(lazyRetry(componentImport, name, retriesLeft - 1, interval));
        }, interval);
      }).then((component: any) => component);
    })
  );
}

/**
 * Preload a lazy-loaded component
 */
export function preloadComponent(componentImport: () => Promise<any>) {
  componentImport();
}
