from uuid import UUID

from sqlalchemy.orm import Session

from database.models import Rectangles
from schemas.models import DeleteRectangleResponse, Rectangle, UpdateRectangle, LineSegment

# Check the intersection between Rectangle and Line Segment
# (x1, y1), (x2, y2) two endpoints of the Line Segment
# (a1, b1), (a2, b2) two endpoints of any of Rectangle sides
def intersect(x1, y1, x2, y2, a1, b1, a2, b2):
    denom = (b2-b1)*(x2-x1) - (a2-a1)*(y2-y1)
    if denom == 0: # parallel
        return False
    ua = ((a2-a1)*(y1-b1) - (b2-b1)*(x1-a1)) / denom
    if ua < 0 or ua > 1: # out of range
        return False
    ub = ((x2-x1)*(y1-b1) - (y2-y1)*(x1-a1)) / denom
    if ub < 0 or ub > 1: # out of range
        return False
    
    return True


# @route: /rectangles/create
# @method: POST
def create(db: Session, rectangle: Rectangle):
    db_rectangle = Rectangles(x1=rectangle.x1, y1=rectangle.y1, x2=rectangle.x2, y2=rectangle.y2, x3=rectangle.x3, y3=rectangle.y3, x4=rectangle.x4, y4=rectangle.y4)
    db.add(db_rectangle)
    db.commit()
    db.refresh(db_rectangle)
    return db_rectangle


# @route: /rectangles/get/{id}
# @method: GET
def get_one(db: Session, id: UUID):
    return db.query(Rectangles).filter_by(id=id).one()


# @route: /rectangles/update
# @method: PATCH
def update(db: Session, rectangle: UpdateRectangle):
    update_query = {
                        Rectangles.x1: rectangle.x1, Rectangles.y1: rectangle.y1,
                        Rectangles.x2: rectangle.x2, Rectangles.y2: rectangle.y2,
                        Rectangles.x3: rectangle.x3, Rectangles.y3: rectangle.y3,
                        Rectangles.x4: rectangle.x4, Rectangles.y4: rectangle.y4
                    }
    db.query(Rectangles).filter_by(id=rectangle.id).update(update_query)
    db.commit()
    return db.query(Rectangles).filter_by(id=rectangle.id).one()


# @route: /rectangles/get/{id}
# @method: DELETE
def delete(db: Session, id: UUID):
    rectangle = db.query(Rectangles).filter_by(id=id).all()
    if not rectangle:
        return DeleteRectangleResponse(detail="Does not Exist")
    db.query(Rectangles).filter_by(id=id).delete()
    db.commit()
    return DeleteRectangleResponse(detail="Rectangle Deleted")


# @route: /rectangles/all
# @method: GET
def get_all(db: Session):
    return db.query(Rectangles).all()


# @route: /rectangles/intersect
# @method: POST
def detect_intersect(db: Session, segment: LineSegment):
    rectangles = db.query(Rectangles).all()
    intersecting_rectangles = []

    def check_intersection(side):
        return intersect(segment.x1, segment.y1, segment.x2, segment.y2, *side)

    for rectangle in rectangles:
        sides = [
            (rectangle.x1, rectangle.y1, rectangle.x2, rectangle.y2),
            (rectangle.x2, rectangle.y2, rectangle.x3, rectangle.y3),
            (rectangle.x3, rectangle.y3, rectangle.x4, rectangle.y4),
            (rectangle.x4, rectangle.y4, rectangle.x1, rectangle.y1),
        ]
        if any(check_intersection(side) for side in sides):
            intersecting_rectangles.append(rectangle)

    return intersecting_rectangles