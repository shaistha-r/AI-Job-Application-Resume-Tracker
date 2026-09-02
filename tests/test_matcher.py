from services.job_matcher import match_resume_to_job

def test_match_score_is_explainable():
    result=match_resume_to_job("Python Flask SQL Git project experience", "Required Python Flask SQL Git Docker")
    assert 0 <= result["score"] <= 100
    assert "Python" in result["matched_skills"]
    assert "Docker" in result["missing_skills"]
    assert "required_skills" in result["breakdown"]
