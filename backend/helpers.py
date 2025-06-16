def position_to_coordinates(position):
        if not 0 <= position <= 8:
            print(f"Position {position} is not valid")
            raise ValueError("Position within single grid must be between 0 and 8")
            
        # Convert 1D index to 2D coordinates
        row = position // 3
        col = position % 3
        return row, col