class LinearBC:

    def __init__(self, edge0, edge1, kind, unity, value, domain, edge, nx, ny):
        self.x0 = edge0[0]
        self.y0 = edge0[1]
        self.x1 = edge1[0]
        self.y1 = edge1[1]
        self.kind = kind
        self.unity = unity
        self.value = value
        self.domain = domain
        self.edge = edge
        self.ny = ny
        self.nx = nx

    def test(self, point):
        # return true if point is within line of BC if c is between a and b
        crossproduct = (point[1] - self.y0) * (self.x1 - self.x0) - (point[0] - self.x0) * (self.y1 - self.y0)

        # compare versus epsilon for floating point values, or != 0 if using integers
        # epsilon is not defined
        if abs(crossproduct) > epsilon:
            return False

        dotproduct = (point[0] - self.x0) * (self.x1 - self.x0) + (point[1] - self.y0) * (self.y1 - self.y0)
        if dotproduct < 0:
            return False

        squaredlengthba = (self.x1 - self.x0) * (self.x1 - self.x0) + (self.y1 - self.y0) * (self.y1 - self.y0)
        if dotproduct > squaredlengthba:
            return False

        return True
