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
        
    
class Bullet(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__("class/spaceship/red_bullet.png")
        self.center_x = x
        self.center_y = y + 24  # شلیک از بالای سفینه
        self.width = 50
        self.height = 100
        self.speed = 10
        self.angle = 270  #چرخش 270 درجه

    def update(self, delta_time: float):
        self.center_y += self.speed
        if self.center_y > 700 + 24:  # حذف تیرهای خارج از صفحه
            self.remove_from_sprite_lists()
            
        
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
    
    
    
class PauseMenu:
    def __init__(self):
        self.paused = False
        self.show_pause_menu = False

    def draw(self):
        if self.paused and self.show_pause_menu:
            arcade.draw_lrbt_rectangle_filled(
                left=400,    # x - width/2
                right=800,   # x + width/2
                top=450,     # y + height/2
                bottom=250,  # y - height/2
                color= arcade.color.DARK_SLATE_BLUE
            )
            arcade.draw_text("Game Paused", 465, 400, arcade.color.WHITE, 36)
            arcade.draw_text("R: Resume", 530, 350, arcade.color.WHITE, 24)
            arcade.draw_text("Q: Quit", 550, 300, arcade.color.WHITE, 24)

    def handle_key_press(self, symbol: int):
        if symbol == arcade.key.ESCAPE:
            self.paused = not self.paused
            self.show_pause_menu = self.paused
            return True
        elif self.paused:
            if symbol == arcade.key.R:
                self.paused = False
                self.show_pause_menu = False
                return True
            elif symbol == arcade.key.Q:
                arcade.exit()
                return True
        return False
    
    
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
        
        self.bullet_list = arcade.SpriteList()  # لیست برای تیرها
        self.bullet_timer = 0  # تایمر برای محدودیت شلیک
        self.bullet_interval = 0.2  # حداقل فاصله زمانی بین شلیک‌ها (ثانیه)
        
        # متغیرها برای مدیریت پایان بازی
        self.game_over = False
        self.game_over_timer = 0
        self.game_over_delay = 3.0  # ۳ ثانیه تاخیر برای نمایش پیام
        
        # اضافه کردن منوی توقف
        self.pause_menu = PauseMenu()
        
    #show   
    def on_draw(self):
        self.clear()
        self.background_list.draw()  # رسم پس زمینه
        self.spaceship_list.draw()  # رسم سفینه
        self.spaceship_enemy_list.draw()  # رسم سفینه دشمن
        self.bullet_list.draw()  # رسم تیرها
        
        # نمایش پیام پایان بازی
        if self.game_over:
            arcade.draw_text("Game Over☠️!", 400, 350, arcade.color.RED, 48)
            
        # رسم منوی توقف
        self.pause_menu.draw()
            
        
    def on_key_press(self, symbol:int, modifiers:int):
        #print(symbol)
        # ابتدا ورودی رو به منوی توقف می‌فرستیم
        if self.pause_menu.handle_key_press(symbol):
            return  # اگه منو ورودی رو پردازش کرد، ادامه نمی‌دیم
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
            elif symbol == arcade.key.SPACE:
                # شلیک تیر
                if self.bullet_timer <= 0:
                    bullet = Bullet(self.me.center_x, self.me.center_y)
                    self.bullet_list.append(bullet)
                    self.bullet_timer = self.bullet_interval
               
    def on_key_release(self, symbol: int, modifiers: int):
        if not self.pause_menu.paused and not self.game_over:
        # توقف حرکت هنگام رها کردن کلید
            if symbol in (arcade.key.LEFT, arcade.key.A, arcade.key.RIGHT, arcade.key.D):
                self.me.Hold_the_button("X")
            if symbol in (arcade.key.UP, arcade.key.W, arcade.key.DOWN, arcade.key.S):
                self.me.Hold_the_button("Y")
                
    def on_update(self ,delta_time: float):
        if not self.pause_menu.paused and not self.game_over:
            # به‌روزرسانی موقعیت سفینه
            self.spaceship_list.update()
            self.spaceship_enemy_list.update()
            self.bullet_list.update()  # به‌روزرسانی تیرها
            
            # محدود کردن سفینه به مرزهای صفحه
            self.me.Limit(self.width ,self.height)
            
            
            self.enemy_spawn_timer += delta_time
            if self.enemy_spawn_timer > self.enemy_spawn_interval:
                enemy = Enemy(self.width, self.height)
                self.spaceship_enemy_list.append(enemy)
                self.enemy_spawn_timer = 0
                self.enemy_spawn_interval = random.uniform(0.5, 2.0)  # فاصله تصادفی
                
            # به‌روزرسانی تایمر شلیک
            if self.bullet_timer > 0:
                self.bullet_timer -= delta_time
                
            # حرکت دشمنان
            self.enemy.move(self.spaceship_enemy_list)
                
            # حذف دشمنان خارج از صفحه
            self.enemy.delete_enemy(self.spaceship_enemy_list)
    

            # بررسی برخورد تیر با دشمنان
            for bullet in self.bullet_list:
                hit_list = arcade.check_for_collision_with_list(bullet, self.spaceship_enemy_list)
                if hit_list:
                    bullet.remove_from_sprite_lists()  # حذف تیر
                    for enemy in hit_list:
                        enemy.remove_from_sprite_lists()  # حذف دشمن
                
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