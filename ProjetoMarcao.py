import pygame as pg,os,random
from tkinter import simpledialog

raio_bolinha = 30
crescendo = True

pygame.init()

relogio = pygame.time.Clock()
icone  = pygame.image.load("recursos/icone.png")
iron = pygame.image.load("recursos/personagem.png")
fundo = pygame.image.load("recursos/fundo.png")
fundoStart = pygame.image.load("recursos/fundoStart.png")
fundoDead = pygame.image.load("recursos/fundoDead.png")
missel = pygame.image.load("recursos/fireball.png")
dragao = pygame.image.load("recursos/dragon.png")

tamanho = (800,600)
tela = pygame.display.set_mode( tamanho ) 
pygame.display.set_caption("Escape do dragão")
pygame.display.set_icon(icone)
fireSound = pygame.mixer.Sound("recursos/fireball.wav")
explosaoSound = pygame.mixer.Sound("recursos/explosao.wav")
fonte = pygame.font.SysFont("comicsans",28)
fonteStart = pygame.font.SysFont("comicsans",55)
fonteMorte = pygame.font.SysFont("arial",120)
pygame.mixer.music.load("recursos/passarosound.mp3")

branco = (255,255,255)
preto = (0, 0 ,0 )
amarelo=(255,255,0)

def jogar(nome):
    pygame.mixer.Sound.play(fireSound)
    pygame.mixer.music.play(-1)
    posicaoXPersona = 400
    posicaoYPersona = 400
    movimentoXPersona  = 0
    movimentoYPersona  = 0
    posicaoXMissel = 400
    posicaoYMissel = -240
    posicaoXbabydragon = 400
    posicaoYbabydragon = -240
    velocidadeMissel = 1
    velocidadebabydragon = 1
    pontos = 0
    larguraPersona = 100
    alturaPersona = 100
    larguaMissel  = 50
    alturaMissel  = 165
    larguababydragon  = 100
    alturababydragon  = 80
    dificuldade  = 20
    raio_bolinha = 30
    crescendo = True
    posicaoXdragon = 0
    velocidadedragon = 2
    
    babydragon = pygame.image.load("recursos/babydragon.png")
    babydragon = pygame.transform.scale(babydragon,(100,80))
    dragon = pygame.transform.scale(babydragon,(100,50))
    
    largurafireball = missel.get_width()
    alturafireball = missel.get_width()
    posicaoXfireball = random.randint(0,800 - largurafireball)
    posicaoYfireball = -alturafireball
    velocidadefireball = 5
    
    tela.blit(missel,(posicaoXfireball,posicaoYfireball))
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RIGHT:
                movimentoXPersona = 10
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_LEFT:
                movimentoXPersona = -10
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_RIGHT:
                movimentoXPersona = 0
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_LEFT:
                movimentoXPersona = 0
                
        posicaoXPersona = posicaoXPersona + movimentoXPersona            
        posicaoYPersona = posicaoYPersona + movimentoYPersona            
        
        if posicaoXPersona < 0 :
            posicaoXPersona = 10
        elif posicaoXPersona >550:
            posicaoXPersona = 540
            
        if posicaoYPersona < 0 :
            posicaoYPersona = 10
        elif posicaoYPersona > 473:
            posicaoYPersona = 463
        
            
        tela.fill(branco)
        tela.blit(fundo, (0,0) )
        #pygame.draw.circle(tela, preto, (posicaoXPersona,posicaoYPersona), 40, 0 )
        tela.blit( iron, (posicaoXPersona, posicaoYPersona) )
        
        #escolha = random.[babydragon,missel]
        posicaoXdragon += velocidadedragon
        if posicaoXdragon > 800 or posicaoXdragon < -dragao.get_width():
            velocidadedragon = -velocidadedragon
        tela.blit(dragao,(posicaoXdragon,0))
        
        posicaoYMissel = posicaoYMissel + velocidadeMissel
        if posicaoYMissel > 600:
            posicaoYMissel = -240
            pontos = pontos + 1
            velocidadeMissel = velocidadeMissel + 1
            posicaoXMissel = random.randint(0,800)
            pygame.mixer.Sound.play(fireSound)
            
        posicaoYbabydragon = posicaoYbabydragon + velocidadebabydragon
        if posicaoYbabydragon > 600:
            posicaoYbabydragon = -240
            pontos = pontos + 1
            velocidadebabydragon = velocidadebabydragon + 1
            posicaoXbabydragon = random.randint(0,800)
            pygame.mixer.Sound.play(fireSound)    
        tela.blit( babydragon, (posicaoXbabydragon, posicaoYbabydragon) )
        
        texto = fonte.render(nome+"- Pontos: "+str(pontos), True, branco)
        tela.blit(texto, (10,10))
        
        pixelsPersonaX = list(range(posicaoXPersona, posicaoXPersona+larguraPersona))
        pixelsPersonaY = list(range(posicaoYPersona, posicaoYPersona+alturaPersona))
        pixelsMisselX = list(range(posicaoXMissel, posicaoXMissel + larguaMissel))
        pixelsMisselY = list(range(posicaoYMissel, posicaoYMissel + alturaMissel))
        
        #print( len( list( set(pixelsMisselX).intersection(set(pixelsPersonaX))   ) )   )
        if  len( list( set(pixelsMisselY).intersection(set(pixelsPersonaY))) ) > dificuldade:
            if len( list( set(pixelsMisselX).intersection(set(pixelsPersonaX))   ) )  > dificuldade:
                dead(nome, pontos)
        if crescendo:
            raio_bolinha += 1
            if raio_bolinha >= 50:
                crescendo = False
        else:
            raio_bolinha -= 1
            if raio_bolinha <= 30:
                crescendo = True
        pygame.draw.circle(tela,amarelo,(750,50),raio_bolinha)

        pygame.display.update()
        relogio.tick(60)

def dead(nome, pontos):
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(explosaoSound)
    
    jogadas  = {}
    try:
        arquivo = open("historico.txt","r",encoding="utf-8")
        jogadas = eval(arquivo.read())
        arquivo.close()
    except:
        arquivo = open("historico.txt","w",encoding="utf-8")
        arquivo.close()
 
    jogadas[nome] = pontos   
    arquivo = open("historico.txt","w",encoding="utf-8") 
    arquivo.write(str(jogadas))
    arquivo.close()
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                jogar(nome)

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if buttonStart.collidepoint(evento.pos):
                    jogar(nome)
        tela.fill(branco)
        tela.blit(fundoDead, (0,0))
        buttonStart = pygame.draw.rect(tela, preto, (35,482,750,100),0)
        textoStart = fonteStart.render("RESTART", True, branco)
        tela.blit(textoStart, (400,482))
        textoEnter = fonte.render("Press enter to continue...", True, branco)
        tela.blit(textoEnter, (60,482))
        pygame.display.update()
        relogio.tick(60)
 
def ranking():
    estrelas = {}
    try:
        arquivo = open("historico.txt","r",encoding="utf-8" )
        estrelas = eval(arquivo.read())
        arquivo.close()
    except:
        pass
    
    nomes = sorted(estrelas, key=estrelas.get,reverse=True)
    print(estrelas)
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if buttonStart.collidepoint(evento.pos):
                    start()

        tela.fill(preto)
        buttonStart = pygame.draw.rect(tela, preto, (35,482,750,100),0)
        textoStart = fonteStart.render("BACK TO START", True, branco)
        tela.blit(textoStart, (330,482))
        
        
        posicaoY = 50
        for key,nome in enumerate(nomes):
            if key == 13:
                break
            textoJogador = fonte.render(nome + " - "+str(estrelas[nome]), True, branco)
            tela.blit(textoJogador, (300,posicaoY))
            posicaoY = posicaoY + 30

            
        
        pygame.display.update()
        relogio.tick(60)

def start():
    nome = simpledialog.askstring("fuja do dragão","Nome Completo:")
    
    
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if buttonStart.collidepoint(evento.pos):
                    jogar(nome)
                elif buttonRanking.collidepoint(evento.pos):
                    ranking()

        tela.fill(branco)
        tela.blit(fundoStart, (0,0))
        buttonStart = pygame.draw.rect(tela, preto, (35,482,750,100),0)
        buttonRanking = pygame.draw.rect(tela, preto, (35,50,200,50),0,30)
        textoRanking = fonte.render("Ranking", True, branco)
        tela.blit(textoRanking, (90,50))
        textoStart = fonteStart.render("START", True, branco)
        tela.blit(textoStart, (330,482))

        
        
        pygame.display.update()
        relogio.tick(60)

start()

