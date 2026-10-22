class Solution:
    def dailyTemperatures(self, temperatures: list[int]) -> list[int]:
        days_to_wait = [0] * len(temperatures)
        days_waiting_warmer = []
        for day_temp in enumerate(temperatures):
            i, temp_day_i = day_temp
            while days_waiting_warmer:
                past_day, past_temp = days_waiting_warmer[-1]
                if temp_day_i <= past_temp:
                    break

                days_to_wait[past_day] = i - past_day
                days_waiting_warmer.pop()

            days_waiting_warmer.append(day_temp)

        return days_to_wait
