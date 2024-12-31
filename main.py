from kivymd.app import MDApp

from kivymd.uix.dialog import MDDialog
import mysql.connector
from kivy.lang import Builder

# KV layout
kv = """
FloatLayout:
    MDTextField:
        id: email
        hint_text: "Enter your email"
        mode: "round"
        size_hint_x: 0.85
        pos_hint: {"center_x": 0.5, "center_y": 0.6}
        
    MDRaisedButton:
        text: "Submit"
        size_hint: None, None
        size: "200dp", "50dp"
        pos_hint: {"center_x": 0.5, "center_y": 0.4}
        on_release: app.insert_email()
"""

class DatabaseApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        
        # Load the KV layout
        return Builder.load_string(kv)

        
        

    def insert_email(self):
        email = self.root.ids.email.text  # Get email from MDTextField
        if email:
            try:
                # Connect to MySQL server
                connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",  # Your MySQL password here
                    database="u"  # Replace with your database name
                )

                cursor = connection.cursor()

                # Create the table if it doesn't exist
                table_name = "kishore"  # Replace with your desired table name
                cursor.execute(f"""
                    CREATE TABLE IF NOT EXISTS {table_name} (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        email VARCHAR(255) NOT NULL,
                        password VARCHAR(255) NOT NULL
                    )
                """)
                connection.commit()

                # Insert the email into the table (you can use a default password or get it from input)
                password = "default_password"  # Example default password (you can update this)
                cursor.execute(f"""
                    INSERT INTO {table_name} (email, password)
                    VALUES (%s, %s)
                """, (email, password))

                connection.commit()

                # Show a success dialog
                self.show_dialog("Email inserted successfully!")

                # Close the cursor and connection
                cursor.close()
                connection.close()

            except mysql.connector.Error as err:
                print(f"Error: {err}")
                self.show_dialog(f"Error: {err}")
        else:
            self.show_dialog("Please enter a valid email address.")

    def show_dialog(self, message):
        dialog = MDDialog(
            title="Info",
            text=message,
            size_hint=(0.8, 1),
        )
        dialog.open()

if __name__ == "__main__":
    DatabaseApp().run()
