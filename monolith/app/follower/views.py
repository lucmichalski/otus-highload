from flask import Blueprint, abort, render_template
from flask_login import login_required, current_user
from injector import inject

from app.db.repositories import UserRepository
from app.follower.exceptions import FollowerAlreadyExistsException, FollowerDoesNotExistsException
from app.follower.services import FollowerService

follower = Blueprint('follower', __name__, url_prefix='/follower')


@inject
@follower.route('/<user_id>', methods=['GET'])
@login_required
def index(user_id, repository: UserRepository):
    user = repository.find_one_with_follower(current_user.id, int(user_id))
    if not user:
        abort(404)

    users = repository.find_all_with_follower(user.id, accepted=True)
    return render_template(
        'follower.html',
        item=user.get_info(current_user.id),
        followers=[v.get_info(user_id) for k, v in users.items()],
    )


@inject
@follower.route('/list', defaults={'page': 1}, methods=['GET'])
@follower.route('/list/<page>', methods=['GET'])
@login_required
def list_accepted(page, repository: UserRepository):
    pagination = repository.paginate_all_with_follower(
        current_user.id,
        accepted=True,
        limit=10,
        page=int(page)
    )
    return render_template(
        'follower-list.html',
        title='Followers',
        list=[v.get_info(current_user.id) for k, v in pagination.list.items()],
        pagination=pagination.get_params(),
    )


@inject
@follower.route('/list/all', defaults={'page': 1}, methods=['GET'])
@follower.route('/list/all/<page>', methods=['GET'])
@login_required
def list_all(page, repository: UserRepository):
    pagination = repository.paginate_all_with_follower(
        current_user.id,
        limit=10,
        page=int(page)
    )
    return render_template(
        'follower-list.html',
        title='Profiles',
        list=[v.get_info(current_user.id) for k, v in pagination.list.items()],
        pagination=pagination.get_params(),
    )


@inject
@follower.route('/send/<user_id>', methods=['POST'])
@login_required
def send(user_id, repository: UserRepository, service: FollowerService):
    user = repository.find_one(id=user_id)
    if not user:
        abort(404)
    try:
        service.send(current_user, user)
    except FollowerAlreadyExistsException as e:
        return {'success': False, 'errors': [(str(e))]}
    return {'success': True, 'errors': []}


@inject
@follower.route('/accept/<user_id>', methods=['POST'])
@login_required
def accept(user_id, repository: UserRepository, service: FollowerService):
    user = repository.find_one(id=user_id)
    if not user:
        abort(404)
    try:
        service.accept(current_user, user)
    except FollowerDoesNotExistsException as e:
        return {'success': False, 'errors': [(str(e))]}
    return {'success': True, 'errors': []}
