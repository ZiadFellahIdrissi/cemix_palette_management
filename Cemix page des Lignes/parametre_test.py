def minutes_to_hh_mm(minutes):
    # Calculate the hours and remaining minutes
    hours = int(minutes // 60)
    remaining_minutes = int(minutes % 60)
    
    # Handle the fractional part of minutes
    fractional_minutes = minutes - int(minutes)
    seconds = int(fractional_minutes * 60)

    # Format the result as HH:MM:SS
    hh_mm_ss = f'{hours:02d}:{remaining_minutes:02d}:{seconds:02d}'
    
    return hh_mm_ss

# Example usage:
minutes = 353.64  # A floating-point number of minutes
hh_mm_ss = minutes_to_hh_mm(minutes)
print(hh_mm_ss)  # Output will be '02:15:30' for 135.5 minutes
