import string
import fastmail_exceptions

def template_maker(deli='$'):
    class Temp(string.Template):
        delimiter = deli
    return Temp


class TemplateLoader:
    def __init__(self, delimiter='$', filepath='', keys={}):

        try:
            with open(filepath, 'r') as the_file:
                self.in_text = the_file.read()

            # get instance of customized delimiter template
            template = template_maker(deli=delimiter)
            # input the text
            matcher = template(self.in_text)
            # subsitute
            self.out_text = matcher.substitute(keys)
        except IOError as err:
            raise fastmail_exceptions.TemplateLoadException(message='Error: {0}'.format(err))

    def get_intext(self):
        return self.in_text

    def get_outtext(self):
        return self.out_text


if __name__ == '__main__':

    try:
        t = TemplateLoader(delimiter='>>', filepath='ts.txt', keys={'name': 'mohamad',
                                                                     'age': 22,
                                                                     'language': 'python'})
        print "{0} \n\n{1}".format(t.get_intext(), t.get_outtext())

    except IOError as e:
        print str(e)
