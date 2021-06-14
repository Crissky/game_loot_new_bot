class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    
    def __new__(self, text):
        Color.load_text(text)
        Color.colors = ''
        
        return self
        
    def load_text(text):
        Color.text = text
        
        
    def __mount_string(attribute):
        Color.colors += attribute
        return Color
    
    
    def purple():
        return Color.__mount_string(Color.PURPLE)
    
    
    def cyan():
        return Color.__mount_string(Color.CYAN)
    
    
    def dark_cyan():
        return Color.__mount_string(Color.DARKCYAN)
    
    
    def blue():
        return Color.__mount_string(Color.BLUE)
    
    
    def green():
        return Color.__mount_string(Color.GREEN)
    
    
    def yellow():
        return Color.__mount_string(Color.YELLOW)
    
    
    def red():
        return Color.__mount_string(Color.RED)
    
    
    def underline():
        return Color.__mount_string(Color.UNDERLINE)
    
    
    def bold():
        return Color.__mount_string(Color.BOLD)
    
    
    def clear_colors():
        Color.colors = ''
        return Color
    
    
    def build():
        return Color.colors + Color.text + Color.END
    
    
    def show(end='\n'):
        print(Color.build(), end=end)