import argparse
import csv
from multiprocessing import Pool, cpu_count

class AutoImporter:
    def __init__(self):
        self.installed = set()

    def install(self, package):
        if package not in self.installed:
            print(f"⚠️ [AutoInstaller] Installing missing package: {package}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            self.installed.add(package)

    def try_import(self, package_name, import_as=None, from_import=None):
        try:
            if from_import:
                module = __import__(from_import[0], fromlist=[from_import[1]])
                globals()[from_import[1]] = getattr(module, from_import[1])
            elif import_as:
                module = __import__(package_name)
                globals()[import_as] = module
            else:
                module = __import__(package_name)
                globals()[package_name] = module
        except ImportError:
            self.install(package_name)
            self.try_import(package_name, import_as, from_import)


# Auto-importer instance
auto = AutoImporter()

# External modules
auto.try_import("requests")
auto.try_import("rich", from_import=("rich.progress", "track"))
auto.try_import("rich", from_import=("rich.console", "Console"))


console = Console()

class SubdomainFinder:
    def __init__(self, domain: str, output: str):
        self.domain = domain
        self.output = output
        self.subdomains = set()

    def fetch_subdomains(self):
        url = f"https://crt.sh/?q=%25.{self.domain}&output=json"
        console.print(f"🔎 [cyan]Mengambil data dari [bold]crt.sh[/bold] untuk[/cyan] {self.domain}")
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            for entry in data:
                names = entry.get('name_value', '').split('\n')
                for name in names:
                    if self.domain in name and '*' not in name:
                        self.subdomains.add(name.strip())
            console.print(f"✅ [green]Ditemukan {len(self.subdomains)} subdomain unik.[/green]")
        except Exception as e:
            console.print(f"❌ [red]Gagal mengambil subdomain: {e}[/red]")

    @staticmethod
    def check_single_git(sub):
        base_https = f"https://{sub}/.git/"
        base_http = f"http://{sub}/.git/"
        head_https = f"{base_https}HEAD"
        head_http = f"{base_http}HEAD"

        try:
            resp = requests.get(head_https, timeout=5)
            if resp.status_code == 200 and "ref:" in resp.text:
                return (sub, head_https.replace("/HEAD", ""), resp.status_code)
        except requests.RequestException:
            pass

        try:
            resp = requests.get(head_http, timeout=5)
            if resp.status_code == 200 and "ref:" in resp.text:
                return (sub, head_http.replace("/HEAD", ""), resp.status_code)
        except requests.RequestException:
            pass

        return (sub, head_https.replace("/HEAD", ""), "Not Found or Invalid")

    def check_git_dirs(self):
        console.print("📁 [yellow]Memeriksa direktori .git pada tiap subdomain dengan multiprocessing...[/yellow]")
        subdomains_list = list(self.subdomains)
        results = []
        with Pool(processes=cpu_count()) as pool:
            for result in track(pool.imap_unordered(self.check_single_git, subdomains_list),
                                total=len(subdomains_list),
                                description="🔧 Mengecek .git"):
                results.append(result)
        return results

    def save_to_csv(self, data):
        try:
            with open(self.output, "w", newline="", encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Subdomain", "Git URL", "Status Code"])
                for row in data:
                    writer.writerow(row)
            console.print(f"💾 [green]Data berhasil disimpan ke[/green] [bold]{self.output}[/bold]")
        except Exception as e:
            console.print(f"❌ [red]Gagal menyimpan file CSV: {e}[/red]")

    def run(self):
        self.fetch_subdomains()
        result = self.check_git_dirs()
        self.save_to_csv(result)

def main():
    parser = argparse.ArgumentParser(description="🔍 gitFinder to find .git in subdomain")
    parser.add_argument("url", help="Domain utama (contoh: example.com)")
    parser.add_argument("--output", help="Path output CSV", default="output.csv")

    args = parser.parse_args()

    finder = SubdomainFinder(args.url, args.output)
    finder.run()

if __name__ == "__main__":
    main()
