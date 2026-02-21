import os
import json
import sys
import time
import tkinter as tk
from tkinter import filedialog, messagebox

class App:

    def __init__(self, root):

        self.root = root
        self.root.title("RubinOT SellAll Whitelist Updater")
        self.root.geometry("600x450")
        self.root.resizable(False, False)

        self.ids_path = tk.StringVar()
        self.game_path = tk.StringVar()
        self.status = tk.StringVar()

        # caminho padrão
        self.game_path.set(r"C:\Program Files (x86)\RubinOT 2.0\bin\screenshots")

        self.create_widgets()
        self.set_status("Pronto.", "blue")


    def create_widgets(self):
        padding = {"padx": 10, "pady": 1}

        # Descrição detalhada
        tk.Label(
            self.root,
            text="Como funciona:",
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", padx=10, pady=0)
        tk.Label(
            self.root,
            text=(
                "Opcional: selecione um arquivo JSON personalizado com sua própria lista de IDs.\n"
                "Se nenhum arquivo for selecionado, será utilizada a lista padrão embutida.\n"
                "A lista padrão remove automaticamente itens conhecidos como:\n"
                "• Itens de Imbuements (tibiawiki.com.br/wiki/Imbuements)\n"
                "• Itens de Addons (tibiawiki.com.br/wiki/Itens_de_Addons)\n"
                "• Itens de Weekly Tasks (tibiapal.com/deliveries)\n"
                "• Plasma Rings e itens relacionados\n"
                "• Outros itens especiais conhecidos"
            ),
            font=("Segoe UI", 9),
            fg="#555555",
            justify="left",
            wraplength=560
        ).pack(anchor="w", padx=20, pady=(0, 0))


        # JSON
        tk.Label(
            self.root,
            text="Arquivo JSON com IDs:"
        ).pack(anchor="w", **padding)

        frame_json = tk.Frame(self.root)
        frame_json.pack(fill="x", **padding)
        tk.Entry(frame_json, textvariable=self.ids_path).pack(side="left", fill="x", expand=True)
        tk.Button(frame_json, text="Selecionar", command=self.select_json).pack(side="left", padx=5)


        # Pasta
        tk.Label(
            self.root,
            text=(
                "Como encontrar o caminho correto:\n"
                "1. Abra o RubinOT -> 2. Vá em OPTIONS -> 3. Clique em MISC -> 4. Clique em OPEN SCREENSHOT FOLDER -> 5. Copie o caminho da pasta aberta\n"
                "Exemplo padrão: já está configurado"
            ),
            font=("Segoe UI", 9),
            fg="#555555",
            justify="left",
            wraplength=560
        ).pack(anchor="w", padx=20)

        tk.Label(
            self.root,
            text="Pasta screenshots do RubinOT:"
        ).pack(anchor="w", **padding)

        frame_path = tk.Frame(self.root)
        frame_path.pack(fill="x", **padding)
        tk.Entry(frame_path, textvariable=self.game_path).pack(side="left", fill="x", expand=True)
        tk.Button(frame_path, text="Selecionar", command=self.select_folder).pack(side="left", padx=5)


        # Botões
        frame_buttons = tk.Frame(self.root)
        frame_buttons.pack(pady=15)
        tk.Button(frame_buttons, text="Iniciar", width=15, command=self.start).pack(side="left", padx=5)

        # Status
        tk.Label(self.root, text="Status:").pack(anchor="w", **padding)
        # tk.Label(self.root, textvariable=self.status, fg="blue").pack(anchor="w", **padding)
        self.status_label = tk.Label(
            self.root,
            textvariable=self.status,
            fg="blue",
            font=("Segoe UI", 9, "bold")
        )
        self.status_label.pack(anchor="w", **padding)

    def set_status(self, text, color="blue"):
        self.status.set(text)
        self.status_label.config(fg=color)

        self.root.update_idletasks()

    def load_default_ids_backup(self):

        try:

            if getattr(sys, 'frozen', False):

                base_path = sys._MEIPASS

            else:

                base_path = os.path.dirname(os.path.abspath(__file__))


            default_file = os.path.join(base_path, "default_ids.json")


            with open(default_file, "r", encoding="utf-8") as f:
                return json.load(f)


        except Exception as e:
            self.set_status(f"Erro ao carregar lista padrão: {str(e)}","red")
            return []

    def load_default_ids(self):
        try:

            if getattr(sys, 'frozen', False):
                base_path = sys._MEIPASS
            else:
                base_path = os.path.dirname(os.path.abspath(__file__))

            default_file = os.path.join(base_path, "default_ids.jsonc")

            with open(default_file, "r", encoding="utf-8") as f:

                lines = []

                for line in f:
                    # remove comentários //
                    line = line.split("//")[0]
                    lines.append(line)

                clean_json = "".join(lines)

                data = json.loads(clean_json)

                # junta todas listas
                ids = []

                for category in data.values():
                    ids.extend(category)

                return list(dict.fromkeys(ids))

        except Exception as e:

            self.set_status(
                f"Erro ao carregar default_ids: {str(e)}",
                "red"
            )

            return []

    def select_json(self):
        file = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json")]
        )

        if file:
            self.ids_path.set(file)


    def select_folder(self):

        folder = filedialog.askdirectory()

        if folder:
            self.game_path.set(folder)


    def find_bin_folder(self, path, timeout=2):

        start_time = time.monotonic()

        path = os.path.abspath(path)

        while True:

            # timeout check
            if time.monotonic() - start_time > timeout:

                raise TimeoutError("Timeout procurando pasta bin")

            if path.lower().endswith("bin"):

                return path

            parent = os.path.dirname(path)

            # chegou na raiz e não achou
            if parent == path:

                raise FileNotFoundError("Pasta bin não encontrada")

            path = parent


    def update_whitelist(self, whitelist_path, ids):

        with open(whitelist_path, "r", encoding="utf-8") as f:
            current = json.load(f)

        original_len = len(current)

        current.extend(ids)

        current = list(dict.fromkeys(current))

        added = len(current) - original_len

        with open(whitelist_path, "w", encoding="utf-8") as f:
            json.dump(current, f, indent=4)

        return added


    def start(self):

        try:

            ids_file = self.ids_path.get()
            folder = self.game_path.get()
            if not folder:
                self.set_status("Selecione a pasta.", "red")
                return

            self.set_status("Carregando IDs...", "blue")

            if ids_file and os.path.exists(ids_file):
                self.set_status("Carregando IDs do JSON selecionado...")
                with open(ids_file, "r", encoding="utf-8") as f:
                    ids = json.load(f)

            else:
                self.set_status("Carregando lista padrão...")
                ids = self.load_default_ids()

            if not ids or len(ids) == 0:
                self.set_status("Nenhum ID encontrado para adicionar.", "orange")
                return

            self.set_status("Procurando pasta characterdata...")

            try:

                bin_path = self.find_bin_folder(folder, timeout=2)

            except TimeoutError:

                self.set_status(
                    "Erro: Timeout. Pasta bin não encontrada em 2 segundos.",
                    "red"
                )
                return

            except FileNotFoundError:

                self.set_status(
                    "Erro: Pasta bin não encontrada.",
                    "red"
                )
                return

            except Exception as e:

                self.set_status(
                    f"Erro inesperado: {str(e)}",
                    "red"
                )
                return
            

            characterdata = os.path.join(bin_path, "characterdata")
            if not os.path.exists(characterdata):
                self.set_status("Erro: Pasta characterdata não encontrada.", "red")
                return

            total_files = 0
            total_added = 0

            for folder_name in os.listdir(characterdata):

                folder_path = os.path.join(characterdata, folder_name)

                whitelist = os.path.join(folder_path, "sellAllWhitelist.json")

                if os.path.exists(whitelist):

                    added = self.update_whitelist(whitelist, ids)

                    total_files += 1
                    total_added += added

            if total_files == 0:
                self.set_status("Nenhum arquivo encontrado.", "orange")
                return

            self.set_status(f"Concluído. {total_files} arquivos atualizados.", "green")

        except Exception as e:
            self.set_status(f"Erro: {str(e)}", "red")


    def cancel(self):

        self.set_status("Cancelado")

def main():

    root = tk.Tk()

    app = App(root)

    root.mainloop()


if __name__ == "__main__":
    main()