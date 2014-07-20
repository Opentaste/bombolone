# Require any additional compass plugins here.
require 'compass'
require 'compass-h5bp'
require 'bootstrap-sass'

# Set this to the root of your project when deployed:
http_path = "/"
css_dir = "static/css"
sass_dir = "static/sass"
images_dir = "static/layout"
javascripts_dir = "static/js"

# You can select your preferred output style here (can be overridden via the command line):
output_style = :expanded #:compressed or :nested or :compact or :compressed

# To enable relative paths to assets via compass helper functions. Uncomment:
# relative_assets = true

# To disable debugging comments that display the original location of your selectors. Uncomment:
line_comments = false

module Sass::Script::Functions
  
  # Custom str_index function for use in Sass
  def str_index(string, substring)
    assert_type string, :String
    assert_type substring, :String
    index = string.value.index(substring.value) || -1
    Sass::Script::Number.new(index + 1)
  end
  declare :str_index, [:string, :substring]
  
  # Custom list_files function for use in Sass (used for sprites)
  def list_files(path)
    return Sass::Script::List.new(
      Dir.glob(path.value).map! { |x| Sass::Script::String.new(x) },
      :comma
    )
  end
  
end
