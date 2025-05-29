import arcade
import random

#pip install arcade



class Spaceship(arcade.Sprite):
    def __init__(self ,w):
        super().__init__("class/spaceship/spaceship.png")
        self.center_x = w // 2  #موقعیت x
        self.center_y = 50      #موقعیت y
        self.width = 48         #عرض سفینه
        self.height = 48        #ارتفاع سفینه
        self.speed = 8          # سرعت سفینه
        
        
    def move(self ,direction):
        if direction == "L":
            self.change_x = -self.speed
        elif direction == "R":
            self.change_x = self.speed
        elif direction == "U":
            self.change_y = self.speed
        elif direction == "D":
            self.change_y = -self.speed
            
    def Hold_the_button(self ,direction):
        if direction == "X":
            self.change_x = 0
        if direction == "Y":
            self.change_y = 0
        
    def Limit(self ,width ,height):
        self.center_x = max(24, min(width - 24, self.center_x))
        self.center_y = max(24, min(height - 24, self.center_y))
        
    
    
class Enemy(arcade.Sprite):
    def __init__(self ,w ,h):
        super().__init__("class/spaceship/icons8-spaceship-60.png")
        self.center_x = random.randint(0,w)   #موقعیت x
        self.center_y = h + 24   #موقعیت y
        self.angle = 180  #چرخش 180 درجه
        self.width = 48   #عرض سفینه
        self.height = 48  #ارتفاع سفینه
        self.speed = 3
        
        
    def move(self , spaceship_enemy_list):
        for enemy in spaceship_enemy_list:
                enemy.center_y -= enemy.speed
                
    def delete_enemy(self ,spaceship_enemy_list):
        for enemy in spaceship_enemy_list:
                if enemy.center_y < -24:
                    enemy.remove_from_sprite_lists()
    
    
class Game(arcade.Window):
    def __init__(self):
        super().__init__(width=1200, height=700 ,title="Space_Ship")
        arcade.set_background_color(arcade.color.PINE_GREEN)
        # بارگذاری عکس خودت به‌عنوان پس‌زمینه
        self.background = arcade.Sprite("class\spaceship\Large jpeg_Universe_Bkg_1_D.jpg", center_x=400, center_y=300)
        # تنظیم مقیاس برای هماهنگی با اندازه پنجره
        scale_width = 1800 / self.background.width
        scale_height = 1000 / self.background.height
        self.background.scale = max(scale_width, scale_height)
        # ایجاد لیست اسپرایت‌ها برای پس زمینه
        self.background_list = arcade.SpriteList()
        self.background_list.append(self.background)
        
        # ایجاد لیست اسپرایت‌ها برای سفینه
        self.spaceship_list = arcade.SpriteList()
        self.me = Spaceship(self.width)
        self.spaceship_list.append(self.me)
        
        
        #  ایجاد لیست اسپرایت‌ها برای سفینه دشمن
        self.spaceship_enemy_list = arcade.SpriteList()
        self.enemy = Enemy(self.width ,self.height)
        self.spaceship_enemy_list.append(self.enemy)
        
        # زمان‌بندی برای تولید دشمن
        self.enemy_spawn_timer = 0
        self.enemy_spawn_interval = 1.0
        
        # متغیرها برای مدیریت پایان بازی
        self.game_over = False
        self.game_over_timer = 0
        self.game_over_delay = 3.0  # ۳ ثانیه تاخیر برای نمایش پیام
        
    #show   
    def on_draw(self):
        self.clear()
        self.background_list.draw()  # رسم پس زمینه
        self.spaceship_list.draw()  # رسم سفینه
        self.spaceship_enemy_list.draw()  # رسم سفینه دشمن
        
        # نمایش پیام پایان بازی
        if self.game_over:
            arcade.draw_text("Game Over!", 400, 350, arcade.color.RED, 48)
        
    def on_key_press(self, symbol:int, modifiers:int):
        #print(symbol)
        if not self.game_over:
        # حرکت با کلیدهای جهت‌دار یا WASD
            if symbol == arcade.key.LEFT or symbol == arcade.key.A:
                self.me.move("L")
            elif symbol == arcade.key.RIGHT or symbol == arcade.key.D:
                self.me.move("R")
            elif symbol == arcade.key.UP or symbol == arcade.key.W:
                self.me.move("U")
            elif symbol == arcade.key.DOWN or symbol == arcade.key.S:
                self.me.move("D")
              
    def on_key_release(self, symbol: int, modifiers: int):
        # توقف حرکت هنگام رها کردن کلید
        if symbol in (arcade.key.LEFT, arcade.key.A, arcade.key.RIGHT, arcade.key.D):
            self.me.Hold_the_button("X")
        if symbol in (arcade.key.UP, arcade.key.W, arcade.key.DOWN, arcade.key.S):
            self.me.Hold_the_button("Y")
                
    def on_update(self ,delta_time: float):
        if not self.game_over:
            # به‌روزرسانی موقعیت سفینه
            self.spaceship_list.update()
            self.spaceship_enemy_list.update()
            
            # محدود کردن سفینه به مرزهای صفحه
            self.me.Limit(self.width ,self.height)
            
            
            self.enemy_spawn_timer += delta_time
            if self.enemy_spawn_timer > self.enemy_spawn_interval:
                enemy = Enemy(self.width, self.height)
                self.spaceship_enemy_list.append(enemy)
                self.enemy_spawn_timer = 0
                self.enemy_spawn_interval = random.uniform(0.5, 2.0)  # فاصله تصادفی
                
            # حرکت دشمنان
            self.enemy.move(self.spaceship_enemy_list)
                
            # حذف دشمنان خارج از صفحه
            self.enemy.delete_enemy(self.spaceship_enemy_list)
    
                
            # بررسی برخورد
            if arcade.check_for_collision_with_list(self.me, self.spaceship_enemy_list):
                self.game_over = True
                print("برخورد! بازی تمام شد.")
            
            # مدیریت تایمر پایان بازی
        if self.game_over:
            self.game_over_timer += delta_time
            if self.game_over_timer >= self.game_over_delay:
                 arcade.exit()  # بستن بازی بعد از ۳ ثانیه
            
    
    
    
    
window = Game()


arcade.run()