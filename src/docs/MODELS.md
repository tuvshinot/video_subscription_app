Model architect planing

Membership
    -slug EX: /course-number-1/
    -type (free, pro, enterprice)
    -price
    -stripe plan id

UserMemberShip
    -user (FK to user)
    -stripe custumer id
    -membership type (fk to member ship)

Subscription 
    -user member ship
    -stripe subscription id (FK to User membership)
    -active

Course
    -slug
    -title
    -desc
    -allowed memberhips (FK to membership)

Lesson
    -slug
    -title
    -Course (FK to course)
    -position
    -video
    -thumbnail
