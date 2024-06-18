import pygame as pg

def ejecutar_menu():
    pg.font.init()
    negro = (0, 0, 0)
    blanco = (255, 255, 255)
    ventana = pg.display.get_surface()
    
    if ventana is None:
        print("Error: La superficie de pantalla no está disponible")
        return
    
    font = pg.font.Font("assets/fonts/Space-Grotesk/SpaceGrotesk-Medium.ttf", 32)
    text_frame = font.render("Presiona Espacio para comenzar", True, blanco)
    text_rect = text_frame.get_rect(center=(ventana.get_width() // 2, ventana.get_height() // 2))
    
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                pg.quit()
                exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    running = False
        
        ventana.fill(negro)
        ventana.blit(text_frame, text_rect)
        pg.display.flip()
    
    print("Menu cerrado, iniciando juego.")

