class PersonalityAssessment:
    """
    A DISC personality assessment implementation.
    DISC stands for:
    - D: Dominance
    - I: Influence
    - S: Stabilité 
    - C: Sérieux
    """

    def __init__(self):
        """Initialize the assessment with empty scores."""
        self.scores = {
            "Dominance": 0,
            "Influence": 0,
            "Stabilité": 0,
            "Sérieux": 0
        }

    def calculate_scores(self, answers):
        """
        Calculate DISC scores based on questionnaire answers.
        
        Args:
            answers (dict): Dictionary containing answers for all 20 questions
                          Keys are question numbers (1-20)
                          Values are scores (1-5)
        
        The questions are grouped as follows:
        - Questions 1-5: Dominance (D)
        - Questions 6-10: Influence (I)
        - Questions 11-15: Stabilité (S)
        - Questions 16-20: Sérieux (C)
        """
        # Questions 1-5 contribute to D score
        self.scores["Dominance"] = sum(answers[f"p{i}"] for i in range(1, 6))
        
        # Questions 6-10 contribute to I score
        self.scores["Influence"] = sum(answers[f"p{i}"] for i in range(6, 11))
        
        # Questions 11-15 contribute to S score
        self.scores["Stabilité"] = sum(answers[f"p{i}"] for i in range(11, 16))
        
        # Questions 16-20 contribute to C score
        self.scores["Sérieux"] = sum(answers[f"p{i}"] for i in range(16, 21))

    def get_personality_type(self):
        """
        Determine the dominant personality type(s) based on scores.
        
        Returns:
            list: One or more personality types that are dominant.
                 If there's a tie, returns multiple types.
        """
        # Get unique scores and sort them in descending order
        unique_scores = sorted(set(self.scores.values()), reverse=True)
        
        # Get personality types with the highest score
        dominant_types = []
        
        # If only one highest score exists
        if len(unique_scores) == 4:
            # Get the type with the highest score
            for disc_type, score in self.scores.items():
                if score == unique_scores[0]:
                    dominant_types.append(disc_type)
        else:
            # Handle ties - get all types that share the highest score
            for disc_type, score in self.scores.items():
                if score == unique_scores[0]:
                    dominant_types.append(disc_type)
            
            # If we have exactly two types with equal scores
            if len(dominant_types) == 2:
                # Return both types in both possible orders
                return [f"{dominant_types[0]} / {dominant_types[1]}", 
                       f"{dominant_types[1]} / {dominant_types[0]}"]
        
        return dominant_types

def process_form_data(form_data):
    """
    Process the form data and return personality assessment results.
    
    Args:
        form_data: Flask form data containing personality questionnaire answers
        with keys 'q1' through 'q20' and values being one of:
        'Jamais', 'Rarement', 'Parfois', 'Souvent', 'Toujours'
        
    Returns:
        dict: Dictionary containing DISC scores and personality type
    """
    assessment = PersonalityAssessment()
    
    # Map French responses to numeric values
    value_map = {
        'Jamais': 1,
        'Rarement': 2,
        'Parfois': 3,
        'Souvent': 4,
        'Toujours': 5
    }
    
    # Convert form data to the expected format
    answers = {}
    for i in range(1, 21):
        form_key = f"p{i}"
        if form_key in form_data:
            answers[f"p{i}"] = value_map[form_data[form_key]]
    
    assessment.calculate_scores(answers)
    
    return {
        "scores": assessment.scores,
        "personality_type": assessment.get_personality_type()
    }

class DonAssessment:
    def __init__(self):
        self.scores = {chr(ord('A') + i): 0 for i in range(14)}  # 'A' to 'N'

    def calculate_scores(self, answers):
        # Each don has 8 questions, e.g., A: d1, d15, d29, ..., d99
        for idx, don in enumerate(self.scores.keys()):
            self.scores[don] = sum(
                answers.get(f"d{q}", 0) for q in [
                    1 + idx, 15 + idx, 29 + idx, 43 + idx, 57 + idx, 71 + idx, 85 + idx, 99 + idx
                ]
            )

    def get_top_dons(self):
        sorted_scores = sorted(self.scores.items(), key=lambda x: x[1], reverse=True)
        top_score = sorted_scores[0][1]
        dons_grand = [k for k, v in self.scores.items() if v == top_score]
        # Get top 2 unique scores
        unique_scores = sorted(set(self.scores.values()), reverse=True)
        dons = []
        for score in unique_scores[:2]:
            dons += [k for k, v in self.scores.items() if v == score]
        return dons, dons_grand

def process_don_form_data(form_data):
    """
    Process the don form data and return don assessment results.
    Args:
        form_data: Flask form data containing don questionnaire answers
        with keys 'd1' through 'd112' and values being one of:
        'Pas du tout', 'Parfois', 'Souvent', 'Toujours'
    Returns:
        dict: Dictionary containing don scores, dons, and grandDon
    """
    assessment = DonAssessment()
    # Map French responses to numeric values
    value_map = {
        'Pas du tout': 0,
        'Parfois': 1,
        'Souvent': 2,
        'Toujours': 3
    }
    # Convert form data to the expected format
    answers = {}
    for i in range(1, 113):
        form_key = f"d{i}"
        if form_key in form_data:
            answers[form_key] = value_map[form_data[form_key]]
    assessment.calculate_scores(answers)
    dons, dons_grand = assessment.get_top_dons()
    return {
        "don_scores": assessment.scores,
        "dons": dons,
        "dons_grand": dons_grand
    }