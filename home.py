from tkinter import *
from tkinter import ttk
from chart import ChartFrame
from weight import WeighInFrame
from datetime import date
import subprocess

class HomeFrame(ttk.Frame):    

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()
        # Ensure cart display reflects current app cart when frame is created
        try:
            self.update_cart_display()
        except Exception:
            pass

    def create_widgets(self):
        # Main container with minimal padding for small screen
        main_container = ttk.Frame(self)
        main_container.pack(fill=BOTH, expand=True, padx=8, pady=8)
        
        # Header: compact name + calories in one row
        header_frame = ttk.Frame(main_container)
        header_frame.pack(fill=X, pady=(0, 8))

        self.label_header = ttk.Label(header_frame, text="Junie Birum", style='Header.TLabel', cursor='hand2')
        self.label_header.pack(side=LEFT, padx=(0, 10))
        self.label_header.bind("<Button-1>", lambda event: self.master.attributes("-fullscreen", False))
        
        # Calories display inline with header
        self.total_calories_label = ttk.Label(header_frame, 
            text=f"{date.today()}     💊 {self.master.calories_today['bova_taken']}/2     💧 {self.master.calories_today['drops_taken']}/4     🤢 {self.master.calories_today['nausea_taken']}/1    {self.master.get_total_calories()}/250 cal   ", 
            style='Subheader.TLabel')
        self.total_calories_label.pack(side=RIGHT)

        # (Tabs removed) — Chart button moved to footer below

        # Content area where either the home content or the chart will appear
        content_area = ttk.Frame(main_container)
        content_area.pack(fill=BOTH, expand=True)

        # Home content is a frame we can hide/show when switching tabs
        self.home_content_frame = ttk.Frame(content_area)
        self.home_content_frame.pack(fill=BOTH, expand=True)

        # Chart frame (initially not packed) — pass callback to return to home
        self.chart_frame = ChartFrame(content_area, app=self.master, show_home_callback=lambda: self.show_tab('home'))
        # Weigh-in frame (initially not packed)
        self.weighin_frame = WeighInFrame(content_area, app=self.master, show_home_callback=lambda: self.show_tab('home'))

        # Cart display section - compact (moved into home content)
        cart_frame = ttk.Frame(self.home_content_frame, style='Card.TFrame')
        cart_frame.pack(fill=X, pady=(10, 25))
        
        cart_label = ttk.Label(cart_frame, text="Cart:", style='Subheader.TLabel')
        cart_label.pack(side=LEFT, padx=8, pady=6)
        
        self.cart_display = ttk.Label(cart_frame, text="(empty)", style='Card.TLabel')
        self.cart_display.pack(side=LEFT, padx=8, pady=6, fill=X, expand=True)
        
        # Item buttons arranged in a compact 2-row grid (no scrolling)
        items_frame = ttk.Frame(self.home_content_frame)
        items_frame.pack(fill=X, padx=4, pady=(0, 8))

        # Configure 6 equal-width columns so buttons share space (2 rows max)
        for i in range(5):
            items_frame.columnconfigure(i, weight=1)

        # Row 0
        self.wetFoodButton = ttk.Button(items_frame, text="🍣 Wet Food",
            command=lambda: self.master.add_to_cart("wet_quantity", self.master.wet_default_quantity),
            style='Accent.TButton')
        self.wetFoodButton.grid(row=0, column=0, sticky='nsew', padx=4, pady=4)

        self.dryFoodButton = ttk.Button(items_frame, text="🧆 Dry Food",
            command=lambda: self.master.add_to_cart("dry_quantity", self.master.dry_default_quantity),
            style='Accent.TButton')
        self.dryFoodButton.grid(row=0, column=1, sticky='nsew', padx=4, pady=4)

        minnow_btn = ttk.Button(items_frame, text="🐟 Minnow",
            command=lambda: self.add_extra_item("minnow_quantity"),
            style='Accent.TButton')
        minnow_btn.grid(row=0, column=2, sticky='nsew', padx=4, pady=4)

        egg_btn = ttk.Button(items_frame, text="🥚 Egg",
            command=lambda: self.add_extra_item("egg_quantity"),
            style='Accent.TButton')
        egg_btn.grid(row=0, column=3, sticky='nsew', padx=4, pady=4)

        # New item: Churu (tube) - default 0.5, increments by 0.5
        churu_btn = ttk.Button(items_frame, text="🧴 Churu",
            command=lambda: self.add_extra_item("churu_quantity"),
            style='Accent.TButton')
        churu_btn.grid(row=0, column=4, sticky='nsew', padx=4, pady=4)

        # New item: Greenie - default 1, increments by 1
        greenie_btn = ttk.Button(items_frame, text="🟢 Greenie",
            command=lambda: self.add_extra_item("greenie_quantity"),
            style='Accent.TButton')
        greenie_btn.grid(row=1, column=0, sticky='nsew', padx=4, pady=4)

        # Row 1
        giblet_btn = ttk.Button(items_frame, text="🦴 Giblet",
            command=lambda: self.add_extra_item("giblet_quantity"),
            style='Accent.TButton')
        giblet_btn.grid(row=1, column=1, sticky='nsew', padx=4, pady=4)

        bova_btn = ttk.Button(items_frame, text="💊 Bova",
            command=lambda: self.add_medicine("bova_taken"),
            style='Accent.TButton')
        bova_btn.grid(row=1, column=2, sticky='nsew', padx=4, pady=4)

        drops_btn = ttk.Button(items_frame, text="💧 Drops",
            command=lambda: self.add_medicine("drops_taken"),
            style='Accent.TButton')
        drops_btn.grid(row=1, column=3, sticky='nsew', padx=4, pady=4)

        nausea_btn = ttk.Button(items_frame, text="🤢 Nausea Meds",
            command=lambda: self.add_medicine("nausea_taken"),
            style='Accent.TButton')
        nausea_btn.grid(row=1, column=4, sticky='nsew', padx=4, pady=4)

        # columns 4 and 5 on row 1 are intentionally left empty for spacing
        
        # Footer with compact action buttons: small Exit to left of Checkout
        footer_frame = ttk.Frame(self.home_content_frame)
        footer_frame.pack(fill=X, pady=(0, 0))

        # Button container aligned to the right so actions don't span full width
        button_frame = ttk.Frame(footer_frame)
        button_frame.pack(fill=X, pady=(0, 0))

        # Checkout button
        self.checkoutButton = ttk.Button(button_frame, text="🛒 CHECKOUT",
            command=self.master.checkout_cart, style='NarrowAccent.TButton')
        self.checkoutButton.pack(fill=X, pady=(20,0))

        # Chart and Weigh In side-by-side row
        row_frame = ttk.Frame(button_frame)
        row_frame.pack(fill=X, pady=(4,0))

        self.chartButton = ttk.Button(row_frame, text="📈 CHART",
            command=lambda: self.show_tab('chart'), style='NarrowAccent.TButton')
        self.chartButton.pack(side=LEFT, fill=X, expand=True, padx=(0, 4))

        self.weighButton = ttk.Button(row_frame, text="⚖️ WEIGH IN",
            command=lambda: self.show_weighin(), style='NarrowAccent.TButton')
        self.weighButton.pack(side=LEFT, fill=X, expand=True, padx=(4, 0))

        # self.exitButton = ttk.Button(button_frame, text="EXIT",
        #     command=self.master.quit, style='Small.TButton', width=8)
        # self.exitButton.pack(side=RIGHT, padx=(4,0))


    
    def update_cart_display(self):
        """Update the cart display with current items"""
        if not self.master.cart:
            self.cart_display.config(text="(empty)")
        else:
            icon_map = self.master.get_cart_icon_map()
            cart_items = []
            for item, quantity in self.master.cart.items():
                icon = icon_map.get(item, "")
                cart_items.append(f"{icon} {quantity}x")
            display_text = "  ".join(cart_items)
            self.cart_display.config(text=display_text)
    
    def add_extra_item(self, item):
        """Handle extra item additions"""
        if item == "minnow_quantity":
            self.master.add_to_cart(item, self.master.minnow_default_quantity)
        elif item == "egg_quantity":
            self.master.add_to_cart(item, self.master.egg_default_quantity)
        elif item == "giblet_quantity":
            self.master.add_to_cart(item, self.master.giblet_default_quantity)
        elif item == "churu_quantity":
            self.master.add_to_cart(item, self.master.churu_default_quantity)
        elif item == "greenie_quantity":
            self.master.add_to_cart(item, self.master.greenie_default_quantity)
    
    def add_medicine(self, item):
        """Handle medicine additions"""
        self.master.add_to_cart(item, 1)


    def update_total_calories_label(self):
        self.total_calories_label.config(text=f"{self.master.get_total_calories()} Total Calories Today")

    def show_tab(self, tab):
        """Show either the home content or the chart frame based on the tab name."""
        if tab == 'home':
            try:
                self.chart_frame.pack_forget()
            except Exception:
                pass
            try:
                self.weighin_frame.pack_forget()
            except Exception:
                pass
            self.home_content_frame.pack(fill=BOTH, expand=True)
        else:
            self.home_content_frame.pack_forget()
            # Refresh chart data before showing so recent changes (e.g. new weight) appear
            try:
                self.chart_frame.refresh()
            except Exception:
                pass
            self.chart_frame.pack(fill=BOTH, expand=True)

    def show_weighin(self):
        self.home_content_frame.pack_forget()
        try:
            self.chart_frame.pack_forget()
        except Exception:
            pass
        # Refresh weigh-in state so UI reflects latest saved weight and clears status
        try:
            self.weighin_frame.refresh()
        except Exception:
            pass
        self.weighin_frame.pack(fill=BOTH, expand=True)