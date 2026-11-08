import argparse
import sys
from collections.abc import Sequence

from cachesim.clock import Clock

from .lru import LRU
from .simulator import run_simulation

ALGORITHMS = {
    "lru": LRU,
    "clock": Clock,
}


def parse_args(args: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Кэш-симулятор: исследование алгоритмов замещения страниц."
    )
    parser.add_argument(
        "--algo",
        type=str,
        required=True,
        choices=list(ALGORITHMS.keys()),
        help=f"Алгоритм кэширования (доступные: {', '.join(ALGORITHMS.keys())})",
    )
    parser.add_argument(
        "--capacity",
        type=int,
        required=True,
        help="Емкость кэша (положительное целое число)",
    )
    parser.add_argument(
        "--pages",
        type=int,
        nargs="+",
        required=True,
        help="Трасса обращений к страницам через пробел (например: 1 2 3 1 4)",
    )
    return parser.parse_args(args)


def main() -> None:
    args = parse_args()

    if args.capacity <= 0:
        print(
            f"Ошибка: capacity должен быть > 0, получено {args.capacity}",
            file=sys.stderr,
        )
        sys.exit(1)

    algo_cls = ALGORITHMS[args.algo]
    cache = algo_cls(capacity=args.capacity)

    result = run_simulation(cache, args.pages)

    print(f"hits={result.hits}")
    print(f"misses={result.misses}")
    print(f"total={result.total}")
    print(f"hit_rate={result.hit_rate:.3f}")


if __name__ == "__main__":
    main()