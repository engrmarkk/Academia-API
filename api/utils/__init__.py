def calculate_gpa(scores, units):
    total_grade_points = 0
    total_credits = 0

    for i in range(len(scores)):
        if scores[i] >= 80:
            grade_points = 4.0
        elif scores[i] >= 65:
            grade_points = 3.0
        elif scores[i] >= 55:
            grade_points = 2.0
        elif scores[i] >= 40:
            grade_points = 1.0
        else:
            grade_points = 0.0

        total_grade_points += grade_points * units[i]
        total_credits += units[i]

    gpa = round(total_grade_points / total_credits, 2)

    return gpa


def get_grade(score):
    if score >= 80:
        return 'A'
    elif score >= 65:
        return 'B'
    elif score >= 55:
        return 'C'
    elif score >= 40:
        return 'D'
    else:
        return 'F'
