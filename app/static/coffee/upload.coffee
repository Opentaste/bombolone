UploadCtrl = ($scope, $resource, $rootScope) ->

  $scope.upload_allowed = true

  match_write_recipe = path.match(/^\/write_recipe\/?$/i) or path.match(/^\/write_recipe\/([^\/]+)\/?$/i)
  match_users = path.match(/^\/admin\/users\/([^\/]+)\/?$/i)
  match_settings = path.match(/^\/settings\/profile\/?$/i)

  if match_write_recipe
    console.log "Run write recipe"
    up =
      multiple: true
      module : "recipes"
      action : app["api_path_up"]+"/recipes/upload_image.json"
      recipe : true

  else if match_users or match_settings
    console.log "Run users"
    up =
      multiple: false
      module : 'avatars'
      action : app["api_path_up"]+"/account/upload_avatar.json"
      recipe : false

  $scope.setFile = (element) ->
    $scope.$apply ($scope) ->
      $scope.files = element.files
      __init_upload()
  
  $scope.file = []
  $scope.number_upload = 0

  __upload_supported = ->
    input = d.createElement("input")
    input.type = "file"
    "multiple" of input and typeof File isnt "undefined" and typeof (new XMLHttpRequest()).upload isnt "undefined"

  if __upload_supported() is false
    $scope.upload_allowed = false
    alert("I'm sorry but your browser is old!
      \nIt's not possible upload images by Ajax, please use one of the version is green in this page http://caniuse.com/xhr2")


  # assegno all'evento onchange dell'input una funzione
  __init_upload = () ->
    console.log "Files ===> ", $scope.files
    files_list = $scope.files
    for index in [0...files_list.length]
      item = files_list[index]
      if not up.multiple and $scope.number_upload
        __show_message_error("Attento stai gia caricando un altro file")
      else
        file_data = 
          "index" : index
          "progress" : 0
          "file" : item
          "size" : if item.fileSize? then item.fileSize else item.size
          "name" : if item.fileName? then item.fileName else item.name
        if file_data.file_size > 10000000
          __show_message_error("Attento il file è più grande di 10Mb")
        else
          $scope.file.push file_data
          position = $scope.file.length
          $scope.number_upload += 1
          __load_file($scope.file[position - 1])


  $scope.stop_upload = (index) ->
    if index
      $scope.file[index].xhr.abort()
      $scope.file[index].xhr = null
    else
      for item of $scope.file[index]
        __abort_upload(item)


  __abort_upload = (upload) ->
    if upload? is false
      item.abort()
      item = null


  __load_file = (upload) ->
    upload.xhr = new XMLHttpRequest()
    upload.text = upload.name + "  " + __format_size(upload.size)
    upload.info_show = true
    if up.recipe
      $scope.$parent.recipe.images.push upload
      upload.len = $scope.$parent.recipe.images.length - 1
      upload.show = "/static/recipes/default.jpg"
      upload.description = 
        it: ""
        en: ""
      upload = $scope.$parent.recipe.images[upload.len]
    __start_upload(upload)


  __start_upload = (file) ->
    file.xhr.upload.onprogress = ((file) ->
      # Event listener for while the file is uploading
      (e) ->
        $scope.$apply ->
          percentCompleted = Math.round(e.loaded / e.total * 100)
          if percentCompleted < 1
            file.progress_value = "Uploading..."
          else if percentCompleted is 100
            file.progress_value = "Saving..."
          else
            file.progress_value = percentCompleted + "%"
          file.progress = percentCompleted + "%"
    )(file)


    file.xhr.onload = ((file, index) ->
      # Event listener for when the file completed uploading
      (e) ->
        $scope.$apply ->
          file.progress_value = "Uploaded!"
          data = JSON.parse(e.target.responseText)
          if data.success
            image = data.message
            if up.recipe
              file.progress_value = "Completato  " + __format_size(file.size)
              $scope.$parent.recipe.images[file.len].uploaded = image
              $scope.$parent.recipe.images[file.len].show = "/static/#{up.module}/tmp/#{image}"
              $scope.number_upload -= 1 
            else
              file.progress_value = "Completato  " + __format_size(file.size)
              $scope.$parent.user.image_uploaded = image
              $scope.$parent.user.image_show = "/static/#{up.module}/tmp/#{image}"
              $scope.number_upload -= 1 
            file.info_show = false
          else
            console.log "loose"
            __upload_failed(evt)
    )(file, file.index)


    #upload.xhr.onerror = (evt) ->
    #  return (evt) ->
    #    $scope.$apply( () ->
    #      console.log "fase 6"
    #      console.log "There was an error attempting to upload the file."
    #      error_message = response.split("] - ")[1]
    #      up.error error_message
    #    )
    #    false

    #upload.xhr.onabort = (evt) -> 
    #  return (evt) ->
    #    $scope.$apply( () ->
    #      console.log "fase 7"
    #      $scope.progressVisible = false
    #      console.log "The upload has been canceled by the user or the browser dropped the connection."
    #    )
    #    false

    file.xhr.open "POST", up.action, true
    file.xhr.setRequestHeader "X-Requested-Token", app["token"]
    file.xhr.setRequestHeader "X-Requested-With", "XMLHttpRequest"
    file.xhr.setRequestHeader "X-File-Name", file.name
    file.xhr.setRequestHeader "Content-Type", "application/octet-stream"
    file.xhr.send file.file


  $scope.remove_image = (index) ->
    if up.recipe
      $scope.$parent.recipe.images.splice index, 1
      


  __format_size = (bytes) ->
    i = -1
    loop
      bytes = bytes / 1024
      i++
      break unless bytes > 99
    Math.max(bytes, 0.1).toFixed(1) + ["kB", "MB", "GB", "TB", "PB", "EB"][i]


  __show_message_error = (message) ->
    console.log message
    #$scope.scroll_top()
    #$rootScope.message_show = true
    #$rootScope.message_status = $scope.status_msg(resource.success)
    #$rootScope.message_message = resource.message
    false


UploadCtrl.$inject = ["$scope", "$resource", "$rootScope"]