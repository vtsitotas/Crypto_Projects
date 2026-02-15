import string
from collections import Counter

# Το κρυπτοκείμενο
ciphertext = "SCEELGZSSLCRFPWUTNTSBXAHRCCCMSAGVCAHYOQHQRKAHRTFRSAEFGDEGWOEGWBFVFGUSVEWOEGOALPDRNGGZPSVFOXAUTBNBVVLACESFWUTRQPLSUEATZVKOMNGVREHTVPWNFAUEVBTLOAGGVRZBMNAPESPNVFGBELTUVBTDPKRNDVWJEBSIESUIHZHUWOUZNBOJHIAVTVLPSORZBOAHRPFVLPCNYZNHHNQLCHKOOBGCAWUEHGFBFPNGBWGSKDVGWBFHLZBFROVUYQPRHYOQHQRVIYVZDNUAIGYSNVZTBNBRPARRZSYQLXCYCFACEBSHUWPSFHSVFJRRNGRLOEFVNRGMTURIESUIHZHHJPNTFOLKAHVFWFKVMRGVVFNLVXSVVLAFVBGZLHHZOATYAVAHUWYENESFGTECRCCDLISLCHKOOBGCAWPDRNWALVTURPESPNLBIJASLTRHNZHLSNBVVLABHHGZLRRNFRGAHREDRGWLRJVBSYEORMBFKTUVGCGPNGNHJZPCUGVRQWRBQIPWAWBVRRSZFBESNUOIQROFWUTVAHUGZENESGZLPRBDYWIELBBQLOEXASRGMTURQHJCEVQCALDAAGHBKVUAQSTGAIFGWPSSHRESVVVNGGVVFRTUNHVSTBRLCAVAHRXBRWVFGUWFUBRIROAVPDBAHXFVWNAMBFLWUBWFAKOXACJKVMRCSBHSEGUOGOLRRVHUAUKSBFRPHMCYSGZHTNAMBFLWVYZNYYERGVNLPSNNQAWDTBAKBMSDORKRDSOAGVRLVPBSHUAZCHEJROOEALCHLOIAXHUSAAGGVRSNEBSHJWUTLSWIWOEUNRCJVDHPSQWUOHTVFUPEAPSCZFSVPGNFKMNGVREHTVPGGGTAXRHRFVRGJSALFMRATNEVUFUSCJVDHPSQTPNBZWNDAHRBFREKISSSEWUTVNZNFKIAGSTJHLPNZPMSUFYOJKVFTEOIAAAGVCADHWFBTZGAIBARRUVMCBGVLPOABTJZPTRYWTZAAAQGBGUNBJKUSAIFVHGZHTFUCBLZOARICLVTUVGCSYTBSHUWJUEISJZHTNESGZLBNFWPJLQHVFRELNGFWGZPNXJSPGBLQFSGVVWAGVEWLTUVBTKAHNGOEWMAVEZLFLCRFGNJFFBEGPALNGVTVUYEFROEUOOESCESUYFBFGGMIAISALPNTBFZSAHRZOGAJSBEDUQZIPFCESUYGUWAYHLBAUGZHTYVBRAKOAGHUAUKNCSEKVNPNBTWAAYBBTOPTUBIGSUYBASBXAHRFSGZYERGVRXPRFGCAWPSBOJVGBSGEOVFPNTNBQWEPREWRFJELBIQGUTRKDRUAAYNKLWYHBJSIWYBEVUULOEZNMOWAOTVJRQVUNASJLOEBEMBXWHLFWPKAHRFSQSFSBEANLOEZNHVUZOERBTAUEREWAYAHRFSPGUDGUWAYPSNPSELHIANABMUTBSWALLLYVURFJEBEHNDLNGVBBLOEEJCEVZYBHVNNLTBUOIWHNVDHUSAIFSOVJSYUVUULVDBTCBVYEFROEUOWBEYVVVNGGVVFRTUNHGZLRRVGNFFGBBRRFNIARSEGYSPVSALPSGGVNLJAATSGSSOATCASUIDBTJZPCUVGGZLAIRFNYLFBEVHEHNORWAYZIABHUWYWBERFZLHNFHBZHVRNBVIOITUSELOAAGVNLLVREMBFLIAGVVKYOBZWFUVNFVRRJHBYLOOGCEGUOGLOIFJSZANHGFOLAZAZNHGWYOSRBIAYOAZSALPNGRZYANEAPSVKHMNGHRJVFURFRVPTLGVBKLTJBWQGUTGUWACHRRFISXPCVRBGAAHVAYGZLRRVGNLOIEQQBFZTVGIRFAHRESNLOIEQQBEWOARBGOOIPUWFLOEBASGZHTZNYRKHNRVBFLLIABFNFPSNNQAWDTBATBJDAAGCSSIEGGSEOVRQJSJASLPNZYAAMBGWISAIBAWAGAHREKBJKSLBIUSCEGBVNNLSBZSXAUDBSOQJPVRFCZWRIAQCSSKEFVFRLVFVARBMATUROAKDEENRRKPRRGCSAUDBHHJZHTZNYRKAHVAUFLPCXVTLGBDBAHUSCEGUOGQVUZNMUSCENYZGZLTENWAAUGNARVFAEYYWTWUCRVBGZLWBEZQQVUQBBGZHVRDIRKAIBAGNFKYBHKBFAJHFHSAUDNAGJWYSGUWFAZAUNFQLOIATHBHBTLBIEXPNTRFBFPTVFOZSATRECSLLMCRFNELNGCFBTHBYLHUSAIFNANLAEEBTCJVBNOZLWHRYLHESPNVAURSYLLPVVDKHBBRRPWEEVSAULSJUSGZLRLBIJASLZBHVNHTRVBGZLDVESPLPOABTFUPEAGWSAJRRFSNJJHVGVVFRTUNHNLHSHCSEXPCVNZYWCEYVHVKILRARRVBSRBTFWCEENZGZPNTFHUAZIFACGSUYNGHREWTNGOQWLPNAOYQZIFNHNDSBHGALXLEYVBTAZTUNHNYVOQFQVWUTVFHUSZATESNLKENYCSOOAGJSPSUCNYZPMYIBFWGQPWBAHTGHNLQSRHLRVAHBAATUNBGZHTURKNFASGBYAGDTUROAKDEEFVRKQUFGQHJPOHFVBOAHVAUFLPCXNBQZLWNAHFLVKABKGZLAAFKRJZTBDIRKAIBAGNFKISUSFWLSGUWACZHRJOALZTBEOVKLQHRGGAVNFNBQZLWNAHFLVKABKGZLAAFKRJZTBGVBKLTURBGZLRRFHUWPDRNCSVPSFNHVKMAPGWBFIYGUWFAKOAGARSUACRGFATIFGWPVPSFNHVKMAPGWBFVFGUSJGYLQJSQGUTYVYRLOEJNMGZPNTFOEWPMRNBNUVNFGFHUAIIRRVKZAGVGSSJTVBBGZLIQROPGBLQOSRPWRRFGRVPNGUSJGYDFGVVKPSBXPHLPTUVBXLOIATGPGBLQOSQGUEORHGWYIGUWACAHRESVKHNRNHRJDALGCQGAHVFWGZPNXGVVFNSPBIYVIEVZDEGCEQNZVLALRVBBLOEEJCEVZTURFRAZCBAHVFBAYYMNKSITUHVJYIGNHVGUWURBGZPNTFRBFALBBYDMPTREWTZAAAQWGZPNXGVNLKIFFOGAZFNPHVGUIACFRKLNGQOLKPSNXSLVYIIVBTXVRPRWAYVOQFQVWUTVFHF"

# Αγγλικές συχνότητες γραμμάτων (από το A-Z)
english_freq = {
    'A': 0.08167, 'B': 0.01492, 'C': 0.02782, 'D': 0.04253,
    'E': 0.12702, 'F': 0.02228, 'G': 0.02015, 'H': 0.06094,
    'I': 0.06966, 'J': 0.00153, 'K': 0.00772, 'L': 0.04025,
    'M': 0.02406, 'N': 0.06749, 'O': 0.07507, 'P': 0.01929,
    'Q': 0.00095, 'R': 0.05987, 'S': 0.06327, 'T': 0.09056,
    'U': 0.02758, 'V': 0.00978, 'W': 0.02360, 'X': 0.00150,
    'Y': 0.01974, 'Z': 0.00074
}

def index_of_coincidence(text):
    """Υπολογισμός δείκτη σύμπτωσης (IC) για ένα κείμενο"""
    n = len(text)
    if n < 2:
        return 0.0
    
    freq = Counter(text)
    total = 0
    for char, count in freq.items():
        total += count * (count - 1)
    
    ic = total / (n * (n - 1))
    return ic

def friedman_test(ciphertext, alpha=0.0665):
    """Εφαρμογή Friedman test για εύρεση μήκους κλειδιού"""
    max_key_length = 20  # Μέγιστο μήκος κλειδιού για έλεγχο
    best_rho = 1
    best_avg_ic = 0
    
    for rho in range(1, max_key_length + 1):
        total_ic = 0.0
        valid_columns = 0
        
        # Δημιουργία ρ ομάδων
        for i in range(rho):
            # Δημιουργία ομάδας χαρακτήρων
            group = ciphertext[i::rho]
            if len(group) >= 2:  # Χρειαζόμαστε τουλάχιστον 2 χαρακτήρες για IC
                ic = index_of_coincidence(group)
                total_ic += ic
                valid_columns += 1
        
        if valid_columns == 0:
            continue
            
        avg_ic = total_ic / valid_columns
        
        # Ελέγχουμε πόσο κοντά είναι ο μέσος IC στην αναμενόμενη τιμή
        if abs(avg_ic - alpha) < abs(best_avg_ic - alpha):
            best_avg_ic = avg_ic
            best_rho = rho
    
    return best_rho

def find_key_with_frequency_analysis(ciphertext, key_length):
    """Εύρεση κλειδιού με ανάλυση συχνότητας"""
    key = []
    
    for i in range(key_length):
        # Εξαγωγή της i-οστής ομάδας χαρακτήρων
        group = ciphertext[i::key_length]
        if not group:
            continue
            
        # Υπολογισμός συχνότητας χαρακτήρων στην ομάδα
        freq = Counter(group)
        total_chars = len(group)
        
        # Εύρεση του πιο πιθανού κλειδιού για αυτήν την ομάδα
        best_shift = 0
        best_score = float('-inf')
        
        for shift in range(26):
            score = 0.0
            for char, count in freq.items():
                # Αποκρυπτογράφηση του χαρακτήρα με την τρέχουσα μετατόπιση
                decrypted_char = chr(((ord(char) - ord('A') - shift) % 26) + ord('A'))
                # Προσθήκη στη βαθμολογία με βάση την αγγλική συχνότητα
                score += (count / total_chars) * english_freq.get(decrypted_char, 0)
            
            if score > best_score:
                best_score = score
                best_shift = shift
        
        key.append(chr(best_shift + ord('A')))
    
    return ''.join(key)

def decrypt_vigenere(ciphertext, key):
    """Αποκρυπτογράφηση Vigenere με δεδομένο κλειδί"""
    decrypted = []
    key_length = len(key)
    
    for i, char in enumerate(ciphertext):
        if char in string.ascii_uppercase:
            # Υπολογισμός μετατόπισης
            shift = ord(key[i % key_length]) - ord('A')
            # Αποκρυπτογράφηση χαρακτήρα
            decrypted_char = chr(((ord(char) - ord('A') - shift) % 26) + ord('A'))
            decrypted.append(decrypted_char)
        else:
            decrypted.append(char)
    
    return ''.join(decrypted)

# Κύριο μέρος του προγράμματος
if __name__ == "__main__":
    print("Κρυπτοκείμενο:", ciphertext)
    
    # Βήμα 1: Εύρεση μήκους κλειδιού με Friedman test
    key_length = friedman_test(ciphertext)
    print(f"Ευρεθέν μήκος κλειδιού: {key_length}")
    
    # Βήμα 2: Εύρεση του κλειδιού με ανάλυση συχνότητας
    key = find_key_with_frequency_analysis(ciphertext, key_length)
    print(f"Ευρεθέν κλειδί: {key}")
    
    # Βήμα 3: Αποκρυπτογράφηση
    plaintext = decrypt_vigenere(ciphertext, key)
    print(f"Αποκρυπτογραφημένο κείμενο: {plaintext}")