# Users controller
UsersCtrl = ($scope, $resource, $rootScope) ->

	# Define scope user
	user_value = page["user"] or {}
	$scope.user = 
		_id: user_value["_id"] or ""
		ot_name: user_value["ot_name"] or ""
		email: user_value["email"] or ""
		rank: user_value["rank"] or ""
		lan: user_value["lan"] or ""
		time_zone: user_value["time_zone"] or ""
		name: user_value["name"] or ""
		location: user_value["location"] or ""
		web: user_value["web"] or ""
		description: user_value["description"] or ""
		password: ""
		password_new: ""
		password_check: ""
		image_show: user_value["image_show"] or "/static/avatars/default.jpg"
		image_uploaded: ""
		status: user_value["status"] or 0

	$scope.description_counter = 200

	# Run /admin/users/new/ and /admin/users/ _id /
	if path.match(/^\/admin\/users\/new\/?$/i) or path.match(/^\/admin\/users\/([^\/]+)\/?$/i)
		upload =
			module : "avatars"
			frame_class : "upload_target"
			action : "/upload_avatar/"
			action_iframe : "/upload_avatar_iframe/"
			action_base : "{{ url_for('users.update', _id=_id) }}"


	__init_submit = ->
		$rootScope.message_show = false
		params = $scope.user
		params["token"] = app["token"]
		return params


	# Save
	# ===============================================================
	$scope.save = ->
		params = __init_submit()
		$scope.ajaxAccountUpdate.save params, (resource) ->
			$scope.user = resource.user
			$scope.show_message(resource)


	# New
	# ===============================================================
	$scope.create = ->
		params = __init_submit()
		$scope.ajaxUsersNew.save params, (resource) ->
			$scope.user = resource.user
			$scope.show_message(resource)


	# Update
	# ===============================================================
	$scope.update_profile = ->
		params = __init_submit()
		$scope.ajaxAccountUpdateProfile.save params, (resource) ->
			$scope.user = resource.user
			$scope.show_message(resource)


	$scope.update_account = ->
		params = __init_submit()
		$scope.ajaxAccountUpdateAccount.save params, (resource) ->
			$scope.user = resource.user
			$scope.show_message(resource)


	$scope.update_password = ->
		params = __init_submit()
		$scope.ajaxAccountUpdatePassword.save params, (resource) ->
			$scope.user = resource.user
			$scope.show_message(resource)
 

UsersCtrl.$inject = ["$scope", "$resource", "$rootScope"]