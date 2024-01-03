import pygame
class Button:
    def __init__(self, window, text, x, y, width, height, enabled, state=None):
        self.window = window
        self.text = text
        self.x_pos = x
        self.y_pos = y
        self.width = width
        self.height = height
        self.enabled = enabled
        self.state = state
        self.block  = pygame.transform.scale(pygame.image.load('images/block.png').convert_alpha(), (self.height , self.height-10))
    
    def change_text(self, new_text):
        self.text = new_text
        
    def draw(self, font_size):
        font = pygame.font.Font('freesansbold.ttf', font_size)
        button_text = font.render(self.text, True, 'black')
        button_rect = pygame.rect.Rect((self.x_pos-self.width//2, self.y_pos-self.height//2), (self.width, self.height))

        if self.enabled:
            # if self.check_hover():
            #     pygame.draw.rect(self.window, 'blue', button_rect, 0, 5)
            # else:
            #     pygame.draw.rect(self.window, 'light gray', button_rect, 0, 5)
         
            if self.check_click():
                pygame.draw.rect(self.window, 'gray', button_rect, 0, 5)
            else:
                pygame.draw.rect(self.window, 'light gray', button_rect, 0, 5)
            text_rect = button_text.get_rect(center=button_rect.center)
            self.window.blit(button_text, text_rect)

        else:
            pygame.draw.rect(self.window, 'gray', button_rect, 0, 5)
            self.window.blit(self.block, (self.x_pos - 22, self.y_pos -21))

        pygame.draw.rect(self.window, 'black', button_rect, 2, 5)
        # self.window.blit(button_text, (self.x_pos-self.width//2+padding, self.y_pos-self.height//2+padding))

        # text_rect = button_text.get_rect(center=button_rect.center)  # Đặt văn bản vào giữa hình chữ nhật

        # Hiển thị văn bản
        
    def check_click(self, scale_x=1, scale_y=1):
        mouse_pos = pygame.mouse.get_pos()
        # print(mouse_pos)
        left_click = pygame.mouse.get_pressed()[0]
        
        button_rect = pygame.rect.Rect((self.x_pos* scale_x-self.width//2, self.y_pos*scale_y-self.height//2), (self.width, self.height))
        if left_click and button_rect.collidepoint(mouse_pos) and self.enabled:
            
            return True
        else:
            return False

    # scale lấy màn hình lớn hơn chia màn hình bé hơn
    def check_hover(self, scale_x=1, scale_y=1):
        mouse_pos = pygame.mouse.get_pos()
        # print(mouse_pos)
        button_rect = pygame.rect.Rect((self.x_pos* scale_x-self.width//2, self.y_pos*scale_y-self.height//2), (self.width, self.height))
        if button_rect.collidepoint(mouse_pos) and self.enabled:
            return True
        else:
            return False
