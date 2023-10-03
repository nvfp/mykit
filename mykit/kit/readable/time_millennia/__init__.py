## dev-docs: this is the next version of mykit.kit.time.get_dur (this will be deprecated soon)


## TODO: finish this soon
# def time_millennia(
#     __secs: float,
#     /,
#     short: bool = True,
#     include_ms: bool = False,
#     days_in_month: int = 30
# ) -> str:
#     months, _r = divmod(__secs, 3600*24*days_in_month)
#     days, _r = divmod(_r, 3600*24)
#     hours, _r = divmod(_r, 3600)
#     minutes, seconds = divmod(_r, 60)

#     months = int(months)
#     days = int(days)
#     hours = int(hours)
#     minutes = int(minutes)

#     seconds = round(seconds, 3)  # round to milliseconds
#     if not include_ms:
#         seconds = round(seconds)

#     parts = []
#     if short:
#         if months > 0:
#             if months == 1:
#                 parts.append('1 month')
#             else:
#                 parts.append(f'{months} months')
#         if days > 0:
#             if days == 1:
#                 parts.append('1 day')
#             else:
#                 parts.append(f'{days} days')
#         if hours > 0:
#             if hours == 1:
#                 parts.append('1 hr')
#             else:
#                 parts.append(f'{hours} hrs')
#         if minutes > 0:
#             if minutes == 1:
#                 parts.append('1 min')
#             else:
#                 parts.append(f'{minutes} mins')
#         if seconds == 0:
#             if parts == []:
#                 parts.append('0 sec')
#         elif seconds == 1:
#             parts.append('1 sec')
#         else:
#             parts.append(f'{seconds} secs')
#     else:
#         parts.extend((
#             f'{months} months',
#             f'{days} days',
#             f'{hours} hrs',
#             f'{minutes} mins',
#             f'{seconds} secs'
#         ))

#     return ' '.join(parts)