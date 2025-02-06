from fastapi import APIRouter
from fastapi import  HTTPException
from models import QuestionBase,Question,Choice
from database import db_dependency

# Create router instance for question-related endpoints
router = APIRouter( prefix="/question",tags=["questions"])

@router.post("/")
async def create_question(question: QuestionBase, db: db_dependency):
    """
    Create a new question with associated choices
    Args:
        question (QuestionBase): Question data including choices
        db (Session): Database session dependency
    Returns:
        None
    """
    # Create new Question record
    db_question = Question(question_text=question.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)

    # Create Choice records for each choice in the question
    for choise in question.choices:
        db_choise = Choice(
            choice_text=choise.choice_text, 
            is_correct=choise.is_correct, 
            question_id=db_question.id
        )
        db.add(db_choise)
    db.commit()

@router.get("/{question_id}")
async def get_question(question_id: int, db: db_dependency):
    """
    Get a specific question by ID
    Args:
        question_id (int): ID of the question to retrieve
        db (Session): Database session dependency
    Returns:
        Question: Question object if found
    Raises:
        HTTPException: If question is not found
    """
    # Query database for question matching the ID
    result = db.query(Question).filter(Question.id == question_id).first()
    # Raise 404 if question not found
    if not result:
        raise HTTPException(status_code=404, detail="Question not found")
    return result



