class CodeOwner:
    '''
    This is the documentation for the owner of a this Python code file.

    :param name: The name of the code owner
    :type name: str
    :param email: The email address of the code owner
    :type email: str
    :param github: The GitHub username of the code owner
    :type github: str
    '''
    name = 'Saint Heraud'
    github = 'bigprogramme'
    email = None
    def __init__(self):
        pass

    def contact(self):
        '''Returns the contact information for the code owner

        :returns: A string containing the contact information
        :rtype: str
        '''
        return f'Owner Contact Information:\n     Name: {self.name}\n     Email: {self.email}\n     GitHub: {self.github}'
    
print(CodeOwner().contact())