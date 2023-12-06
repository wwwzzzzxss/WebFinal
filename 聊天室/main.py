import pygame
import sys
import os
import random
import math

import login_module



def main():
    #####################################################################
    if login_module.start_login_interface() == True:
    #####################################################################

        # 初始化 Pygame
        pygame.init()
        pygame.display.set_caption("網路撿紅點")
        # 設置遊戲視窗尺寸
        screen_width = 1600
        screen_height = 900
        card_width = 180
        card_height = 270
        screen = pygame.display.set_mode((screen_width, screen_height))


        # 加載背景圖片
        background = pygame.image.load('BG.png')
        background = pygame.transform.scale(background, (screen_width, screen_height))
        screen.blit(background, (0, 0))
        pygame.display.flip()
        # 設置字體
        font = pygame.font.Font(None, 36)




        back_of_card = pygame.image.load('Back.png')
        back_of_card = pygame.transform.scale(back_of_card, (card_width, card_height))  # 假設卡牌的大小為180x270
        back_of_card_pos = (screen_width - back_of_card.get_width() - 50, screen_height / 2 - back_of_card.get_height() / 2)
        # 加載並縮放撲克牌圖像
        def load_and_scale_card_image(card_name, new_width=card_width, new_height=card_height):
            image = pygame.image.load(os.path.join('card_img', card_name + '.png'))
            return pygame.transform.scale(image, (new_width, new_height))

        # 創建撲克牌牌組
        def create_deck():
            suits = ['S', 'H', 'D', 'C']
            values = list(range(1, 14))  # 1到13代表A到K
            deck = [suit + str(value) for suit in suits for value in values]
            return deck

        # 從牌組中隨機發牌
        def deal_hand(deck, num_cards):
            return random.sample(deck, num_cards)

        def deal_animation(screen, hand_cards, start_pos, end_pos, speed = 200):
            for card_name in hand_cards:
                card = load_and_scale_card_image(card_name)
                x, y = start_pos
                end_x, end_y = end_pos

                angle = math.atan2(end_y - y, end_x - x)
                dx = math.cos(angle) * speed
                dy = math.sin(angle) * speed


                while x > end_x or y < end_y:
                    screen.blit(background, (0, 0))
                    for animation_shown_card in animation_shown_cards:
                        screen.blit(animation_shown_card['image'], animation_shown_card['pos'])

                    screen.blit(card, (x, y))

                    pygame.display.flip()
                    x += dx if x > end_x else 0
                    y += dy if y < end_y else 0

                animation_shown_cards.append({'image': card, 'pos': (end_x, end_y)})

        # 創建並發牌
        deck = create_deck()
        hand_cards = deal_hand(deck, 12)  # 隨機選取12張牌作為手牌

        # 遊戲循環
        running = True
        played_cards = []  # 存放打出的牌


        screen.blit(background, (0, 0))
        screen.blit(back_of_card, back_of_card_pos)

        clock = pygame.time.Clock()
        card_spacing = 100
        hand_area_start = 50
        hand_area_y = screen_height - 280  

        end_positions = [(hand_area_start + i* card_spacing, hand_area_y) for i in range(len(hand_cards))]
        animation_shown_cards = []


        for i, card_name in enumerate(hand_cards):
            deal_animation(screen, [card_name], back_of_card_pos, end_positions[i])


        
        while running:
            
            # 繪製背景
            screen.blit(background, (0, 0))
            screen.blit(back_of_card, back_of_card_pos)

            active_card_index = None  # 被選中的牌索引
            hand_card_rects = []

            

            mouse_x, mouse_y = pygame.mouse.get_pos()

            # 顯示手牌
            for i, card_name in enumerate(hand_cards):
                card = load_and_scale_card_image(card_name)
                card_rect = card.get_rect(topleft=(50 + i * card_spacing, screen_height - card.get_height() - 10))


                # 先檢查是否為最右邊一張  再檢查滑鼠是否在牌的主要部分上方
                if i == len(hand_cards) - 1:
                    if card_rect.collidepoint(mouse_x,mouse_y):
                        active_card_index = i
                else:
                    if card_rect.collidepoint(mouse_x, mouse_y) and (mouse_x < card_rect.right - card_spacing // 1.25):
                        active_card_index = i
                    
                # 根據活躍牌索引處理牌的顯示
                if i == active_card_index:
                    card_rect.y -= 20  # 將活躍的牌向上移動

                hand_card_rects.append(card_rect)
                screen.blit(card, card_rect)

            # 顯示打出的牌
            for i, played_card in enumerate(played_cards):
                card = load_and_scale_card_image(played_card)
                screen.blit(card, (300 + i * 60, 200))  # 可以調整這裡的位置來改變牌桌上牌的顯示方式

            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # 出牌並顯示在牌桌上
                    
                    if active_card_index is not None:

                        if active_card_index > len(hand_cards) -1:
                            print(active_card_index ,"pop index out of range")
                        else:
                            
                            played_card = hand_cards.pop(active_card_index)
                            played_cards.append(played_card)
            # 更新遊戲畫面
            pygame.display.flip()
            

        # 退出 Pygame
        pygame.quit()
        sys.exit()

    ###############################################

if __name__ == "__main__":
    #cProfile.run("main()")
    main()