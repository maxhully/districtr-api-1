from flask import Blueprint, json, jsonify, request

from ..auth import authenticate, get_current_user
from ..exceptions import ApiException
from ..result import ApiResult
from ..models import Plan, db
from ..schemas import PlanSchema, PlanSchemaOut

bp = Blueprint("plans", __name__)

plans_schema = PlanSchema(
    only=(
        "id",
        "name",
        "created_at",
        "modified_at",
        "user",
        "units_id",
        "problem_id",
        "place_id",
    ),
    many=True,
)
plan_schema = PlanSchema()
plan_schema_out = PlanSchemaOut()


@bp.route("/", methods=["POST"])
@authenticate
def new_plan():
    data = request.get_json()

    name = data["name"]
    serialized = json.dumps(data["assignment"])
    place_id = data["place_id"]
    problem_id = data["problem_id"]
    units_id = data["units_id"]
    parts = data.get("parts", None)
    if parts is not None:
        parts = json.dumps(parts)

    plan = Plan(
        name=name,
        serialized=serialized,
        place_id=place_id,
        problem_id=problem_id,
        units_id=units_id,
        user=get_current_user(),
        parts=parts,
    )

    db.session.add(plan)
    db.session.commit()
    return jsonify(id=plan.id), 201


@bp.route("/", methods=["GET"])
def list_plans():
    """List all plans."""
    plans = Plan.query.all()
    records = plans_schema.dump(plans)
    return jsonify(records)


@authenticate
def list_my_plans():
    user = get_current_user()
    records = plans_schema.dump(user.plans)
    return ApiResult(records)


@bp.route("/<int:id>", methods=["GET"])
def get_plan(id):
    plan = Plan.query.get_or_404(id)
    return jsonify(plan_schema_out.dump(plan))


@bp.route("/<int:id>", methods=["PATCH", "PUT"])
@authenticate
def update_plan(id):
    plan = Plan.query.get_or_404(id)

    user = get_current_user()
    if not plan.belongs_to(user):
        raise ApiException("You are not authorized to edit this resource.", 403)

    data = request.get_json()
    plan.update(
        name=data.get("name", None), serialized=json.dumps(data.get("serialized", None))
    )
    db.session.commit()

    return "", 204


@bp.route("/<int:id>", methods=["DELETE"])
@authenticate
def delete_plan(id):
    plan = Plan.query.get_or_404(id)

    user = get_current_user()
    if not plan.belongs_to(user):
        raise ApiException("You are not authorized to delete this resource.", 403)

    db.session.delete(plan)
    db.session.commit()

    return "", 204
