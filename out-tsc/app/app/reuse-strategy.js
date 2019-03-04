var CustomReuseStrategy = (function () {
    function CustomReuseStrategy() {
        this.routesToCache = [''];
        this.storedRouteHandles = new Map();
    }
    // Decides if the route should be stored
    CustomReuseStrategy.prototype.shouldDetach = function (route) {
        return this.routesToCache.indexOf(route.routeConfig.path) > -1;
    };
    // Store the information for the route we're destructing
    CustomReuseStrategy.prototype.store = function (route, handle) {
        this.storedRouteHandles.set(route.routeConfig.path, handle);
    };
    // Return true if we have a stored route object for the next route
    CustomReuseStrategy.prototype.shouldAttach = function (route) {
        return this.storedRouteHandles.has(route.routeConfig.path);
    };
    // If we returned true in shouldAttach(), now return the actual route data for restoration
    CustomReuseStrategy.prototype.retrieve = function (route) {
        return this.storedRouteHandles.get(route.routeConfig.path);
    };
    // Reuse the route if we're going to and from the same route
    CustomReuseStrategy.prototype.shouldReuseRoute = function (future, curr) {
        return future.routeConfig === curr.routeConfig;
    };
    return CustomReuseStrategy;
}());
export { CustomReuseStrategy };
//# sourceMappingURL=reuse-strategy.js.map