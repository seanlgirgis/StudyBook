# 004. Class 2 - Find the Torsional Angle

## Source
HackerRank Python - Classes

## Problem Summary
Given four 3D points `A`, `B`, `C`, and `D`, calculate the torsional angle between the planes formed by points `A-B-C` and `B-C-D`. Print the answer in degrees rounded to two decimal places.

## Final Accepted Solution
```python
import math

class Points(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __sub__(self, no):
        return Points(self.x - no.x, self.y - no.y, self.z - no.z)

    def dot(self, no):
        return self.x * no.x + self.y * no.y + self.z * no.z

    def cross(self, no):
        return Points(
            self.y * no.z - self.z * no.y,
            self.z * no.x - self.x * no.z,
            self.x * no.y - self.y * no.x
        )

    def absolute(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)


if __name__ == '__main__':
    points = []
    for i in range(4):
        x, y, z = map(float, input().split())
        points.append(Points(x, y, z))

    A, B, C, D = points

    AB = B - A
    BC = C - B
    CD = D - C

    X = AB.cross(BC)
    Y = BC.cross(CD)

    angle = math.acos(X.dot(Y) / (X.absolute() * Y.absolute()))

    print("%.2f" % math.degrees(angle))
```

## Plain-English Explanation
- Build vectors using subtraction between points (`AB`, `BC`, `CD`).
- Use cross products to get normals of the two planes.
- Use the dot product formula to get the angle between those normals.
- Convert radians to degrees with `math.degrees`.
- Format output with two decimal places using `"%.2f"`.

## Sample Inputs and Outputs
- Input:
  - `0 4 5`
  - `1 7 6`
  - `0 5 9`
  - `1 7 2`
- Output: `8.19`

## Mistakes or Reminders
- Use `float` when reading coordinates.
- Do not forget to convert radians to degrees.
- Keep output formatting exact to two decimal places.

## Review Checklist
- [ ] I can explain why cross products are used here.
- [ ] I can compute vector subtraction from 3D points.
- [ ] I can explain dot product angle formula at a high level.
- [ ] I can format decimal output to exactly two places.
