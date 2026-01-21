import argparse
import asyncio
import sys
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("birthday_countdown")


def _parse_birthday_date(date_str: str) -> tuple[int, int]:
    date_str = date_str.strip()

    parts = date_str.split("-")
    if len(parts) != 2:
        raise ValueError("Formato inválido. Use apenas mês e dia (MM-DD ou M-D), sem ano.")

    month_str, day_str = parts
    if not (month_str.isdigit() and day_str.isdigit()):
        raise ValueError("Formato inválido. Use apenas mês e dia (MM-DD ou M-D), sem ano.")

    month = int(month_str)
    day = int(day_str)

    if month == 2 and day == 29:
        return month, day

    try:
        datetime(2001, month, day)
    except ValueError:
        raise ValueError("Data inválida. Use apenas mês e dia (MM-DD ou M-D), sem ano.")

    return month, day


def _next_birthday_at_midnight(now: datetime, month: int, day: int) -> datetime:
    tz = now.tzinfo
    if tz is None:
        raise ValueError("'now' must be timezone-aware")

    year = now.year

    def _build_target(y: int) -> datetime:
        try:
            return datetime(y, month, day, 0, 0, 0, tzinfo=tz)
        except ValueError:
            if month == 2 and day == 29:
                return datetime(y, 2, 28, 0, 0, 0, tzinfo=tz)
            raise

    candidate = _build_target(year)
    if candidate <= now:
        candidate = _build_target(year + 1)
    return candidate


def _format_timedelta(delta: timedelta) -> str:
    total_seconds = int(delta.total_seconds())
    if total_seconds < 0:
        total_seconds = 0

    days, rem = divmod(total_seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, seconds = divmod(rem, 60)
    return f"{days}d {hours}h {minutes}m {seconds}s"


def _format_timedelta_pt(delta: timedelta) -> str:
    total_seconds = int(delta.total_seconds())
    if total_seconds < 0:
        total_seconds = 0

    days, rem = divmod(total_seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, seconds = divmod(rem, 60)

    parts: list[str] = []
    if days:
        parts.append(f"{days} dia" if days == 1 else f"{days} dias")
    if hours:
        parts.append(f"{hours} hora" if hours == 1 else f"{hours} horas")
    if minutes:
        parts.append(f"{minutes} minuto" if minutes == 1 else f"{minutes} minutos")
    if seconds or not parts:
        parts.append(f"{seconds} segundo" if seconds == 1 else f"{seconds} segundos")
    return ", ".join(parts)


@mcp.tool()
async def time_until_birthday(date: str, timezone: str | None = None) -> str:
    tz = datetime.now().astimezone().tzinfo
    if tz is None:
        tz = ZoneInfo("UTC")

    if timezone:
        tz = ZoneInfo(timezone)

    now = datetime.now(tz)
    month, day = _parse_birthday_date(date)
    target = _next_birthday_at_midnight(now, month, day)
    remaining = target - now

    return (
        f"Now: {now.isoformat()}\n"
        f"Next birthday: {target.date().isoformat()}\n"
        f"Time remaining: {_format_timedelta(remaining)}"
    )


def main() -> None:
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(prog="birthday_countdown.py")
        subparsers = parser.add_subparsers(dest="command", required=True)

        countdown_parser = subparsers.add_parser("countdown")
        countdown_parser.add_argument("date")
        countdown_parser.add_argument("--timezone", default=None)

        args = parser.parse_args()

        if args.command == "countdown":
            tz = datetime.now().astimezone().tzinfo
            if tz is None:
                tz = ZoneInfo("UTC")
            if args.timezone:
                tz = ZoneInfo(args.timezone)

            now = datetime.now(tz)
            try:
                month, day = _parse_birthday_date(args.date)
                target = _next_birthday_at_midnight(now, month, day)
                remaining = target - now
            except ValueError as e:
                print(f"Erro: {e}")
                raise SystemExit(2)

            tz_name = getattr(tz, "key", None) or ("São Paulo (UTC-3)" if args.timezone is None else str(tz))

            print("Contagem regressiva para aniversário!\n")
            print(f"Timezone: {tz_name}\n")
            print(f"Data atual: {now.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Próximo aniversário: {target.strftime('%Y-%m-%d %H:%M:%S')}\n")
            print(f"Falta(m): {_format_timedelta_pt(remaining)}\n")
            return

        raise SystemExit(2)

    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()