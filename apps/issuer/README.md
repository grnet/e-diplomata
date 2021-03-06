# Issuer app

Το Ίδρυμα καλείται να διατηρεί μια επικαιροποιημένη λίστα των Τίτλων Σπουδών που εκδίδει.
Επίσης, διαχειρίζεται τα Αιτήματα προς το Ίδρυμα των Αποφοίτων και έχει τη δυνατότητα επισκόπησης των Κοινοποιήσεων.

## Getting started

We start Issuer server:

```
cd servers\issuer-server
rushx dev
```

and then we start the issuer app

```
cd apps\issuer
rushx dev
```

and then access the service in localhost:3000

# **Ίδρυμα**

### Εγγραφή - Είσοδος

(placeholder)

- Προφίλ
  (placeholder)

### Τίτλοι σπουδών

Το **Ίδρυμα** θα μπορεί να δει όλους τους τίτλους σπουδών που έχει καταχωρίσει. Θα μπορεί επίσης να πατήσει "Προβολή", μεταβαίνοντας στην οθόνη **Προβολή τίτλου**, για να δει περισσότερες πληροφορίες για έναν τίτλο. Τέλος, θα μπορεί να πατήσει το κουμπί "Δημιουργία αιτήματος" για να δημιουργήσει ένα νέο τίτλο.
Τα πεδία που βλέπει είναι:

- Όνομα Τίτλου Σπουδών
- Το είδος του Τίτλου Σπουδών
- Τμήμα/Σχολή
- Ίδρυμα
- Κατάσταση
- Ονοματεπώνυμο **Αποφοίτου**
- Ημερομηνία Έκδοσης

Τα διαθέσιμα φίλτρα που θα έχει στη διάθεσή του το Ίδρυμα είναι:

- Το είδος του τίτλου σπουδών
- Τμήμα/Σχολή
- Ίδρυμα
- Έτος έκδοσης
- Ονοματεπώνυμο **Αποφοίτου**

### Προβολή τίτλου

Το **Ίδρυμα** θα μπορεί να δει τις λεπτομέρειες του τίτλου που έχει καταχωρίσει.
Τα πεδία που βλέπει είναι όλα τα πεδία που αντιστοιχούν στα _Μεταδεδομένα ψηφιακής έκδοσης τίτλου_.

### Δημιουργία τίτλου σπουδών

Το **Ίδρυμα** θα μπορεί να δημιουργήσει ένα νέο τίτλο.
Τα πεδία που θα καταχωρεί είναι:

**Στοιχεία Ψηφιακού Τίτλου** βάσει του σχήματος που έχει οριστεί.

Αντιστοίχως θα καταχωρούνται από το σύστημα τα εξής μεταδεδομένα που αφορούν την ψηφιακή έκδοση του τίτλου

- Μοναδικός κωδικός καταγραφής
- Ημερομηνία καταγραφής
- Κατάσταση

### Αιτήματα απόδοσης τίτλων σπουδών

Το **Ίδρυμα** θα μπορεί προβάλει και να διαχειριστεί τα αιτήματα απόδοσης τίτλων σπουδών που έχουν υποβάλει απόφοιτοι που δεν αντιστοιχίστηκαν αυτόματα με κάποιο τίτλο που έχουν λάβει.
Τα πεδία που βλέπει θα είναι:

- Όνομα Τίτλου Σπουδών
- Το είδος του Τίτλου Σπουδών
- Τμήμα/Σχολή
- Ίδρυμα
- Κατάσταση
- Ονοματεπώνυμο **Αποφοίτου**
- Έτος αποφοίτησης

Το **Ίδρυμα** θα μπορεί να προβάλει το αίτημα απόδοσης τίτλου σπουδών επιλέγοντας το σχετικό κουμπί από όπου και οδηγείται στην οθόνη "Προβολή αιτήματος".

### Προβολή αιτήματος

Το **Ίδρυμα** από την προβολή ενός αιτήματος απόδοσης τίτλου σπουδών ενός **Απόφοιτου** θα μπορεί να δει τα πεδία του αιτήματος:

- Όνομα Τίτλου Σπουδών
- Το είδος του Τίτλου Σπουδών
- Τμήμα/Σχολή
- Ίδρυμα
- Κατάσταση
- Ονοματεπώνυμο **Αποφοίτου**
- Έτος αποφοίτησης

Ακολούθως θα του δίνεται η δυνατότητα για τα αιτήματα που βρίσκονται σε εκκρεμότητα:

- να προχωρήσει σε "Αίτημα απόδοσης τίτλου σπουδών"¨με το κουμπί "Δημιουργία και απόδοση τίτλου"
- να απορρίψει το αίτημα του **Αποφοίτου** εφόσον δεν είναι απόφοιτος βάσει των τηρούμενων στοιχείων

### Κοινοποιήσεις

Το **Ίδρυμα** θα μπορεί προβάλει στην οθόνη του λίστα με τις κοινοποιήσεις τίτλων σπουδών που έχουν δημιουργήσει οι απόφοιτοι προς κάποιο **Φορέα**.
Τα πεδία που βλέπει θα είναι:

- Όνομα Τίτλου Σπουδών
- Το είδος του Τίτλου Σπουδών
- Τμήμα/Σχολή
- Ίδρυμα
- Κατάσταση
- Ονοματεπώνυμο **Αποφοίτου**
- Έτος αποφοίτησης

Το **Ίδρυμα** θα μπορεί να προβάλει την κοινοποίηση τίτλου σπουδών επιλέγοντας το σχετικό κουμπί από όπου και οδηγείται στην οθόνη "Προβολή Κοινοποίησης".

### Προβολή κοινοποίησης

Το **Ίδρυμα** μπορεί να δει επιπλέον στοιχεία για κάθε κοινοποίηση.
Συγκεκριμένα με την προβολή βλέπει τα πεδία για κάθε τίτλο της κοινοποίησης (που έχει εκδοθεί από το συγκεκριμένο Ίδρυμα) όπως ακριβώς περιγράφονται και στην Οθόνη **Προβολή κοινοποίησης** του **Απόφοιτου**.

### Στατιστικά

Δίνεται δυνατότητα εξαγωγής στοιχείων (export) για τις εξής κατηγορίες:

- Πιστοποιήσεις
- Τίτλοι σπουδών
- Αιτήματα

για περαιτέρω στατιστική επεξεργασία από τα Ιδρύματα.

### Επικοινωνία με Γραφείο Αρωγής

(placeholder)
