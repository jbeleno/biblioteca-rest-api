-- Datos de ejemplo para la biblioteca
-- Ejecutar después de crear las tablas

-- Insertar autores
INSERT INTO autores (nombre, created_at) VALUES
('Gabriel García Márquez', NOW()),
('Mario Vargas Llosa', NOW()),
('Isabel Allende', NOW()),
('Jorge Luis Borges', NOW()),
('Julio Cortázar', NOW()),
('Pablo Neruda', NOW()),
('Octavio Paz', NOW()),
('Carlos Fuentes', NOW()),
('Ernest Hemingway', NOW()),
('George Orwell', NOW()),
('Jane Austen', NOW()),
('Virginia Woolf', NOW()),
('Fyodor Dostoevsky', NOW()),
('Leo Tolstoy', NOW()),
('Franz Kafka', NOW()),
('Albert Camus', NOW()),
('Jean-Paul Sartre', NOW()),
('Haruki Murakami', NOW()),
('J.K. Rowling', NOW()),
('Stephen King', NOW()),
('Agatha Christie', NOW()),
('Arthur Conan Doyle', NOW()),
('Edgar Allan Poe', NOW()),
('Mark Twain', NOW()),
('Charles Dickens', NOW());

-- Insertar libros (asumiendo que los IDs de autores empiezan en 1)
INSERT INTO libros (titulo, isbn, ano_publicacion, autor_id, created_at) VALUES
-- Gabriel García Márquez (ID 1)
('Cien años de soledad', '9788437604947', 1967, 1, NOW()),
('El amor en los tiempos del cólera', '9788437604948', 1985, 1, NOW()),
('Crónica de una muerte anunciada', '9788437604949', 1981, 1, NOW()),
('El otoño del patriarca', '9788437604950', 1975, 1, NOW()),
('El general en su laberinto', '9788437604951', 1989, 1, NOW()),

-- Mario Vargas Llosa (ID 2)
('La ciudad y los perros', '9788437604952', 1963, 2, NOW()),
('La casa verde', '9788437604953', 1966, 2, NOW()),
('Conversación en La Catedral', '9788437604954', 1969, 2, NOW()),
('La fiesta del chivo', '9788437604955', 2000, 2, NOW()),
('El sueño del celta', '9788437604956', 2010, 2, NOW()),

-- Isabel Allende (ID 3)
('La casa de los espíritus', '9788437604957', 1982, 3, NOW()),
('Eva Luna', '9788437604958', 1987, 3, NOW()),
('Hija de la fortuna', '9788437604959', 1999, 3, NOW()),
('Inés del alma mía', '9788437604960', 2006, 3, NOW()),

-- Jorge Luis Borges (ID 4)
('Ficciones', '9788437604961', 1944, 4, NOW()),
('El Aleph', '9788437604962', 1949, 4, NOW()),
('El libro de arena', '9788437604963', 1975, 4, NOW()),
('Historia universal de la infamia', '9788437604964', 1935, 4, NOW()),

-- Julio Cortázar (ID 5)
('Rayuela', '9788437604965', 1963, 5, NOW()),
('Bestiario', '9788437604966', 1951, 5, NOW()),
('Final del juego', '9788437604967', 1956, 5, NOW()),
('62 Modelo para armar', '9788437604968', 1968, 5, NOW()),

-- Pablo Neruda (ID 6)
('Veinte poemas de amor y una canción desesperada', '9788437604969', 1924, 6, NOW()),
('Residencia en la tierra', '9788437604970', 1933, 6, NOW()),
('Canto general', '9788437604971', 1950, 6, NOW()),

-- Octavio Paz (ID 7)
('El laberinto de la soledad', '9788437604972', 1950, 7, NOW()),
('Piedra de sol', '9788437604973', 1957, 7, NOW()),

-- Carlos Fuentes (ID 8)
('La región más transparente', '9788437604974', 1958, 8, NOW()),
('La muerte de Artemio Cruz', '9788437604975', 1962, 8, NOW()),
('Aura', '9788437604976', 1962, 8, NOW()),

-- Ernest Hemingway (ID 9)
('El viejo y el mar', '9788437604977', 1952, 9, NOW()),
('Por quién doblan las campanas', '9788437604978', 1940, 9, NOW()),
('Adiós a las armas', '9788437604979', 1929, 9, NOW()),
('Fiesta', '9788437604980', 1926, 9, NOW()),

-- George Orwell (ID 10)
('1984', '9788437604981', 1949, 10, NOW()),
('Rebelión en la granja', '9788437604982', 1945, 10, NOW()),
('Homenaje a Cataluña', '9788437604983', 1938, 10, NOW()),

-- Jane Austen (ID 11)
('Orgullo y prejuicio', '9788437604984', 1813, 11, NOW()),
('Emma', '9788437604985', 1815, 11, NOW()),
('Sentido y sensibilidad', '9788437604986', 1811, 11, NOW()),
('Persuasión', '9788437604987', 1817, 11, NOW()),

-- Virginia Woolf (ID 12)
('Mrs. Dalloway', '9788437604988', 1925, 12, NOW()),
('Al faro', '9788437604989', 1927, 12, NOW()),
('Orlando', '9788437604990', 1928, 12, NOW()),
('Las olas', '9788437604991', 1931, 12, NOW()),

-- Fyodor Dostoevsky (ID 13)
('Crimen y castigo', '9788437604992', 1866, 13, NOW()),
('Los hermanos Karamazov', '9788437604993', 1880, 13, NOW()),
('El idiota', '9788437604994', 1869, 13, NOW()),
('Memorias del subsuelo', '9788437604995', 1864, 13, NOW()),

-- Leo Tolstoy (ID 14)
('Guerra y paz', '9788437604996', 1869, 14, NOW()),
('Ana Karenina', '9788437604997', 1877, 14, NOW()),
('La muerte de Iván Ilich', '9788437604998', 1886, 14, NOW()),

-- Franz Kafka (ID 15)
('La metamorfosis', '9788437604999', 1915, 15, NOW()),
('El proceso', '9788437605000', 1925, 15, NOW()),
('El castillo', '9788437605001', 1926, 15, NOW()),
('América', '9788437605002', 1927, 15, NOW()),

-- Albert Camus (ID 16)
('El extranjero', '9788437605003', 1942, 16, NOW()),
('La peste', '9788437605004', 1947, 16, NOW()),
('La caída', '9788437605005', 1956, 16, NOW()),

-- Jean-Paul Sartre (ID 17)
('La náusea', '9788437605006', 1938, 17, NOW()),
('El ser y la nada', '9788437605007', 1943, 17, NOW()),

-- Haruki Murakami (ID 18)
('Tokio Blues', '9788437605008', 1987, 18, NOW()),
('Kafka en la orilla', '9788437605009', 2002, 18, NOW()),
('1Q84', '9788437605010', 2009, 18, NOW()),
('Norwegian Wood', '9788437605011', 1987, 18, NOW()),

-- J.K. Rowling (ID 19)
('Harry Potter y la piedra filosofal', '9788437605012', 1997, 19, NOW()),
('Harry Potter y la cámara secreta', '9788437605013', 1998, 19, NOW()),
('Harry Potter y el prisionero de Azkaban', '9788437605014', 1999, 19, NOW()),
('Harry Potter y el cáliz de fuego', '9788437605015', 2000, 19, NOW()),
('Harry Potter y la Orden del Fénix', '9788437605016', 2003, 19, NOW()),
('Harry Potter y el misterio del príncipe', '9788437605017', 2005, 19, NOW()),
('Harry Potter y las reliquias de la muerte', '9788437605018', 2007, 19, NOW()),

-- Stephen King (ID 20)
('El resplandor', '9788437605019', 1977, 20, NOW()),
('It', '9788437605020', 1986, 20, NOW()),
('Carrie', '9788437605021', 1974, 20, NOW()),
('Misery', '9788437605022', 1987, 20, NOW()),
('El cementerio', '9788437605023', 1983, 20, NOW()),

-- Agatha Christie (ID 21)
('Asesinato en el Orient Express', '9788437605024', 1934, 21, NOW()),
('Muerte en el Nilo', '9788437605025', 1937, 21, NOW()),
('Diez negritos', '9788437605026', 1939, 21, NOW()),
('El asesinato de Roger Ackroyd', '9788437605027', 1926, 21, NOW()),

-- Arthur Conan Doyle (ID 22)
('Estudio en escarlata', '9788437605028', 1887, 22, NOW()),
('El signo de los cuatro', '9788437605029', 1890, 22, NOW()),
('Las aventuras de Sherlock Holmes', '9788437605030', 1892, 22, NOW()),
('El sabueso de los Baskerville', '9788437605031', 1902, 22, NOW()),

-- Edgar Allan Poe (ID 23)
('El cuervo y otros poemas', '9788437605032', 1845, 23, NOW()),
('Los crímenes de la calle Morgue', '9788437605033', 1841, 23, NOW()),
('El gato negro', '9788437605034', 1843, 23, NOW()),

-- Mark Twain (ID 24)
('Las aventuras de Tom Sawyer', '9788437605035', 1876, 24, NOW()),
('Las aventuras de Huckleberry Finn', '9788437605036', 1884, 24, NOW()),
('Un yanqui en la corte del Rey Arturo', '9788437605037', 1889, 24, NOW()),

-- Charles Dickens (ID 25)
('Oliver Twist', '9788437605038', 1838, 25, NOW()),
('David Copperfield', '9788437605039', 1850, 25, NOW()),
('Grandes esperanzas', '9788437605040', 1861, 25, NOW()),
('Historia de dos ciudades', '9788437605041', 1859, 25, NOW()),
('Cuento de Navidad', '9788437605042', 1843, 25, NOW());

