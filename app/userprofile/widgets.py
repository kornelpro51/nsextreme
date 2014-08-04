from django.contrib.admin.widgets import AdminFileWidget
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
import os
from PIL import Image

class AdminImageWidget(AdminFileWidget):
    default_image = ''
    width = 100
    height = 100
    def __init__(self, attrs=None, default_image='media/images/profile-default.jpg', width=100, height=100):
        self.attrs = attrs or {}
        self.default_image = default_image
        self.width = width
        self.height = height
    def render(self, name, value, attrs=None):
        output = []
        if value and getattr(value, "url", None):

            image_url = value.url
            file_name=str(value)

            # defining the size
            size='100x100'
            size=str(self.width) + 'x' + str(self.height)
            x = self.width
            y = self.height
            try :
                # defining the filename and the miniature filename
                filehead, filetail  = os.path.split(value.path)
                basename, format    = os.path.splitext(filetail)
                miniature           = basename + '_' + size + format
                filename            = value.path
                miniature_filename  = os.path.join(filehead, miniature)
                filehead, filetail  = os.path.split(value.url)
                miniature_url       = filehead + '/' + miniature

                # make sure that the thumbnail is a version of the current original sized image
                if os.path.exists(miniature_filename) and os.path.getmtime(filename) > os.path.getmtime(miniature_filename):
                    os.unlink(miniature_filename)

                # if the image wasn't already resized, resize it
                if not os.path.exists(miniature_filename):
                    image = Image.open(filename)
                    image.thumbnail([x, y], Image.ANTIALIAS)
                    try:
                        image.save(miniature_filename, image.format, quality=100, optimize=1)
                    except:
                        image.save(miniature_filename, image.format, quality=100)

                output.append(u' <div><a href="%s" target="_blank"><img src="%s" alt="%s" /></a></div> %s ' % \
                (miniature_url, miniature_url, miniature_filename, _('Change:')))

            except:
                pass
        else:
            filehead, filetail  = os.path.split(self.default_image)
            miniature           = filetail
            miniature_filename  = os.path.join(filehead, miniature)
            filehead, filetail  = os.path.split(self.default_image)
            miniature_url       = filehead + '/' + miniature

            output.append(u' <div><a href="%s" target="_blank"><img src="%s" alt="%s" width="%dpx" height="%dpx" /></a></div> %s ' % \
            (miniature_url, miniature_url, miniature_filename, self.width, self.height, _('Change:')))
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        #return mark_safe(u'<div>%s</div>' % (str(value)))
        return  mark_safe(u''.join(output))