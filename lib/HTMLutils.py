#!usr/bin/env python

class HTMLutils():
    '''holds helper methods that can build various HTML form types'''

##Headers and footers
    def build_html_header(self):
        header = '</html>'
        return header

    def build_form_header(self, method, action, name):
        form_header = '''
        <form method = %s  action = %s name = %s >
        ''' % (method, action, name)
        return form_header

    def build_form_footer(self):
        form_footer = '</form>'
        return form_footer

    def build_html_footer(self):
        html_footer = '</html>'
        return html_footer



##Form Fields
    def getTextField(self, fieldName, default, readonly = False, className=''):
        ''' given the name of a field and the desired default
        build a simple text form field'''
        
        form_field = '''
           <input id = "%s" type = "text" name = "%s" value = "%s"
              size = "100"
              ''' %(fieldName, fieldName,  default)

        if readonly:
             form_field += ' readonly'

        if className:
            form_field += ' class = "%s"' %className

        form_field += '></input>'

        return form_field

    def getDropDown (self, column, default, options):
        
        form_field = '<select required name = %s>' %column

        #if there is no default build a null option - make it default
        if default == None:
             form_field += '''<option selected = "selected" 
                               value = None>(None)</option>'''

        #check if each option should be set to default else build as normal
        for option in options:
            if option[0] == default:
                form_field +=  '''<option selected = "selected" 
                               value = %d> %s </option>
                               ''' % (option[0], option[1])
            else: 
                form_field += '''<option value = %d> %s</option>
                                      ''' % (option[0], option[1])
        form_field += '</select>'
        return form_field

    def getStaticRadio(self, column, default, options):

        form_field = ''
        # loop through options, identify default, build radio group
        for o in options:
            if o[0] == default:
                form_field += '''<input type = "radio" name = %s value = %d 
                     checked = "true"> %s
                    ''' %(column, o[0], o[1])
            else: form_field += '''<input type = "radio" name = %s 
                                 value = %d > %s
                    ''' %(column, o[0], o[1])
        
        return form_field

    def getJQueryUI (self, column, default, form_type):

        form_field = '''
                   <input id = %s_%s  name = %s value = '%s'>
                  ''' %(column, form_type, column, default)
        return form_field

    def getAutoComplete (self, column, default, className = ''):

        form_field = "<input id = %s_autocomplete  name = %s value = '%s'" \
            %(column, column, default)

        if className:
            form_field += "class = '%s'" %className 

        form_field += '> </input>'

        form_field += ''' 
             <input id = %s_ac_key type = "hidden" name = "%s_id"></input> 
                 ''' %( column, column)
        return form_field


    def getHidden(self, name, value):
        
        hidden = '<input type = "hidden" name = %s value = %s>' \
            % (name, value)

        return hidden

    def getButton(self, value, onClick):
        button = '<input type = "button" value = %s onclick = %s>'\
            % (value, onClick)

        return button
