#include <iostream>
#include <string>
#include <map>
#include <random>
#include <iomanip>

bool isInCircle(double x, double y, double r, double x0, double y0) {
  double dx = x - x0;
  double dy = y - y0;
  return dx * dx + dy * dy <= r * r;
}

int main() {
  std::ios::sync_with_stdio(false);
  std::cin.tie(nullptr);

  double x1, y1, r1;
  double x2, y2, r2;
  double x3, y3, r3;
  std::cin >> x1 >> y1 >> r1 >> x2 >> y2 >> r2 >> x3 >> y3 >> r3;
  int inside = 0;
  std::mt19937_64 rng(123456789);
  int N;
  double left, right, down, up;
  std::cin >> N >> left >> right >> down >> up;
  std::uniform_real_distribution<> disx(left, right);
  std::uniform_real_distribution<> disy(down, up);

  for (int i = 0; i < N; ++i) {
    double x = disx(rng);
    double y = disy(rng);
    if (isInCircle(x1, y1, r1, x, y) &&
        isInCircle(x2, y2, r2, x, y) &&
        isInCircle(x3, y3, r3, x, y))
    {
      inside++;
    }
  }

  double probability = (static_cast<double>(inside) / N) * ((up - down) * (right - left));
  std::cout << std::setprecision(20) << probability;
}

