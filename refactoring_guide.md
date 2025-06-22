# Guia Prático de Refatoração de Código

## 1. Elimine Código Duplicado (DRY - Don't Repeat Yourself)

❌ **Antes:**
```javascript
function calcularDescontoCliente(cliente) {
  if (cliente.tipo === 'VIP') {
    return cliente.totalCompras * 0.2;
  }
  return cliente.totalCompras * 0.1;
}

function calcularDescontoProduto(produto) {
  if (produto.categoria === 'Premium') {
    return produto.preco * 0.2;
  }
  return produto.preco * 0.1;
}
```

✅ **Depois:**
```javascript
function calcularDesconto(valor, isPremium) {
  const descontoPremium = 0.2;
  const descontoPadrao = 0.1;
  return valor * (isPremium ? descontoPremium : descontoPadrao);
}

// Uso
const descontoCliente = calcularDesconto(cliente.totalCompras, cliente.tipo === 'VIP');
const descontoProduto = calcularDesconto(produto.preco, produto.categoria === 'Premium');
```

## 2. Extraia Funções Pequenas e Focadas

❌ **Antes:**
```javascript
function processarPedido(pedido) {
  // Validar pedido
  if (!pedido.itens || pedido.itens.length === 0) {
    throw new Error('Pedido sem itens');
  }
  if (!pedido.cliente) {
    throw new Error('Pedido sem cliente');
  }

  // Calcular total
  let total = 0;
  for (let item of pedido.itens) {
    total += item.preco * item.quantidade;
  }

  // Aplicar desconto
  if (pedido.cliente.tipo === 'VIP') {
    total *= 0.9;
  }

  // Salvar no banco
  database.save(pedido);

  // Enviar email
  emailService.send(pedido.cliente.email, 'Pedido confirmado');

  return total;
}
```

✅ **Depois:**
```javascript
function processarPedido(pedido) {
  validarPedido(pedido);
  const total = calcularTotal(pedido);
  salvarPedido(pedido);
  notificarCliente(pedido.cliente);
  return total;
}

function validarPedido(pedido) {
  if (!pedido.itens?.length) {
    throw new Error('Pedido sem itens');
  }
  if (!pedido.cliente) {
    throw new Error('Pedido sem cliente');
  }
}

function calcularTotal(pedido) {
  const subtotal = pedido.itens.reduce((acc, item) =>
    acc + (item.preco * item.quantidade), 0
  );
  return aplicarDesconto(subtotal, pedido.cliente);
}

function aplicarDesconto(valor, cliente) {
  const desconto = cliente.tipo === 'VIP' ? 0.1 : 0;
  return valor * (1 - desconto);
}

function salvarPedido(pedido) {
  database.save(pedido);
}

function notificarCliente(cliente) {
  emailService.send(cliente.email, 'Pedido confirmado');
}
```

## 3. Use Nomes Descritivos e Evite Comentários Desnecessários

❌ **Antes:**
```javascript
// Função para calcular x
function calc(a, b, t) {
  // Se t for 1, soma
  if (t === 1) {
    return a + b;
  }
  // Se t for 2, subtrai
  else if (t === 2) {
    return a - b;
  }
  // Outros casos
  return 0;
}

const r = calc(10, 5, 1); // resultado
```

✅ **Depois:**
```javascript
const OPERACAO = {
  SOMA: 'soma',
  SUBTRACAO: 'subtracao'
};

function executarOperacao(valor1, valor2, tipoOperacao) {
  switch (tipoOperacao) {
    case OPERACAO.SOMA:
      return valor1 + valor2;
    case OPERACAO.SUBTRACAO:
      return valor1 - valor2;
    default:
      return 0;
  }
}

const resultado = executarOperacao(10, 5, OPERACAO.SOMA);
```

## 4. Aplique o Princípio da Responsabilidade Única (SRP)

❌ **Antes:**
```javascript
class Usuario {
  constructor(nome, email) {
    this.nome = nome;
    this.email = email;
  }

  salvar() {
    // Lógica para salvar no banco
    database.save(this);
  }

  enviarEmail(mensagem) {
    // Lógica para enviar email
    emailService.send(this.email, mensagem);
  }

  validarEmail() {
    // Lógica de validação
    return this.email.includes('@');
  }
}
```

✅ **Depois:**
```javascript
class Usuario {
  constructor(nome, email) {
    this.nome = nome;
    this.email = email;
  }
}

class UsuarioRepository {
  salvar(usuario) {
    return database.save(usuario);
  }

  buscar(id) {
    return database.find(id);
  }
}

class EmailService {
  enviar(email, mensagem) {
    return emailService.send(email, mensagem);
  }
}

class ValidadorEmail {
  validar(email) {
    return email.includes('@') && email.includes('.');
  }
}
```

## 5. Reduza Complexidade Ciclomática

❌ **Antes:**
```javascript
function calcularFrete(peso, distancia, tipo, urgente, fragil) {
  let valor = 0;

  if (peso < 1) {
    if (distancia < 100) {
      valor = 10;
    } else if (distancia < 500) {
      valor = 20;
    } else {
      valor = 30;
    }
  } else if (peso < 5) {
    if (distancia < 100) {
      valor = 15;
    } else if (distancia < 500) {
      valor = 30;
    } else {
      valor = 45;
    }
  } else {
    if (distancia < 100) {
      valor = 20;
    } else if (distancia < 500) {
      valor = 40;
    } else {
      valor = 60;
    }
  }

  if (urgente) valor *= 2;
  if (fragil) valor *= 1.5;

  return valor;
}
```

✅ **Depois:**
```javascript
const TABELA_FRETE = {
  leve: { curta: 10, media: 20, longa: 30 },
  medio: { curta: 15, media: 30, longa: 45 },
  pesado: { curta: 20, media: 40, longa: 60 }
};

function calcularFrete(peso, distancia, opcoes = {}) {
  const categoria = categorizarPeso(peso);
  const faixa = categorizarDistancia(distancia);

  let valor = TABELA_FRETE[categoria][faixa];

  return aplicarTaxasAdicionais(valor, opcoes);
}

function categorizarPeso(peso) {
  if (peso < 1) return 'leve';
  if (peso < 5) return 'medio';
  return 'pesado';
}

function categorizarDistancia(distancia) {
  if (distancia < 100) return 'curta';
  if (distancia < 500) return 'media';
  return 'longa';
}

function aplicarTaxasAdicionais(valor, { urgente, fragil }) {
  if (urgente) valor *= 2;
  if (fragil) valor *= 1.5;
  return valor;
}
```

## 6. Use Early Returns para Reduzir Aninhamento

❌ **Antes:**
```javascript
function processarUsuario(usuario) {
  if (usuario) {
    if (usuario.ativo) {
      if (usuario.email) {
        if (usuario.verificado) {
          // Processar usuário
          return enviarNotificacao(usuario);
        } else {
          return 'Usuário não verificado';
        }
      } else {
        return 'Email não encontrado';
      }
    } else {
      return 'Usuário inativo';
    }
  } else {
    return 'Usuário não existe';
  }
}
```

✅ **Depois:**
```javascript
function processarUsuario(usuario) {
  if (!usuario) return 'Usuário não existe';
  if (!usuario.ativo) return 'Usuário inativo';
  if (!usuario.email) return 'Email não encontrado';
  if (!usuario.verificado) return 'Usuário não verificado';

  return enviarNotificacao(usuario);
}
```

## 7. Extraia Constantes Mágicas

❌ **Antes:**
```javascript
function calcularJuros(valor, meses) {
  if (meses <= 12) {
    return valor * 0.02 * meses;
  } else if (meses <= 24) {
    return valor * 0.015 * meses;
  } else {
    return valor * 0.01 * meses;
  }
}

if (temperatura > 35) {
  ligarArCondicionado();
}
```

✅ **Depois:**
```javascript
const TAXA_JUROS = {
  CURTO_PRAZO: 0.02,
  MEDIO_PRAZO: 0.015,
  LONGO_PRAZO: 0.01
};

const PRAZO = {
  CURTO: 12,
  MEDIO: 24
};

function calcularJuros(valor, meses) {
  if (meses <= PRAZO.CURTO) {
    return valor * TAXA_JUROS.CURTO_PRAZO * meses;
  } else if (meses <= PRAZO.MEDIO) {
    return valor * TAXA_JUROS.MEDIO_PRAZO * meses;
  } else {
    return valor * TAXA_JUROS.LONGO_PRAZO * meses;
  }
}

const TEMPERATURA_MAXIMA_CONFORTAVEL = 35;

if (temperatura > TEMPERATURA_MAXIMA_CONFORTAVEL) {
  ligarArCondicionado();
}
```

## 8. Use Composição ao Invés de Herança Profunda

❌ **Antes:**
```javascript
class Animal {
  mover() { /* ... */ }
}

class Mamifero extends Animal {
  amamentar() { /* ... */ }
}

class Cachorro extends Mamifero {
  latir() { /* ... */ }
}

class CachorroPolicial extends Cachorro {
  farejar() { /* ... */ }
}
```

✅ **Depois:**
```javascript
// Comportamentos como funções ou classes separadas
const movimentacao = {
  mover() { /* ... */ }
};

const amamentacao = {
  amamentar() { /* ... */ }
};

const vocalizacao = {
  latir() { /* ... */ }
};

const rastreamento = {
  farejar() { /* ... */ }
};

// Composição
class CachorroPolicial {
  constructor() {
    Object.assign(this, movimentacao, amamentacao, vocalizacao, rastreamento);
  }
}
```

## 9. Implemente Cache para Operações Custosas

❌ **Antes:**
```javascript
function buscarDadosUsuario(id) {
  // Operação custosa sempre executada
  return database.query(`SELECT * FROM usuarios WHERE id = ${id}`);
}

// Chamadas repetidas
const usuario1 = buscarDadosUsuario(123);
const usuario2 = buscarDadosUsuario(123); // Mesma query novamente
```

✅ **Depois:**
```javascript
const cacheUsuarios = new Map();

function buscarDadosUsuario(id) {
  if (cacheUsuarios.has(id)) {
    return cacheUsuarios.get(id);
  }

  const usuario = database.query(`SELECT * FROM usuarios WHERE id = ${id}`);
  cacheUsuarios.set(id, usuario);

  return usuario;
}

// Ou com decorator/wrapper
function comCache(fn) {
  const cache = new Map();

  return function(...args) {
    const key = JSON.stringify(args);

    if (cache.has(key)) {
      return cache.get(key);
    }

    const resultado = fn.apply(this, args);
    cache.set(key, resultado);

    return resultado;
  };
}

const buscarDadosUsuarioComCache = comCache(buscarDadosUsuario);
```

## 10. Use Async/Await ao Invés de Callbacks Aninhados

❌ **Antes:**
```javascript
function processarDados(callback) {
  buscarUsuario(id, (err, usuario) => {
    if (err) {
      callback(err);
      return;
    }

    buscarPedidos(usuario.id, (err, pedidos) => {
      if (err) {
        callback(err);
        return;
      }

      calcularTotal(pedidos, (err, total) => {
        if (err) {
          callback(err);
          return;
        }

        callback(null, { usuario, pedidos, total });
      });
    });
  });
}
```

✅ **Depois:**
```javascript
async function processarDados() {
  try {
    const usuario = await buscarUsuario(id);
    const pedidos = await buscarPedidos(usuario.id);
    const total = await calcularTotal(pedidos);

    return { usuario, pedidos, total };
  } catch (error) {
    console.error('Erro ao processar dados:', error);
    throw error;
  }
}
```

# Checklist de Refatoração

- [ ] Código duplicado eliminado
- [ ] Funções com responsabilidade única
- [ ] Nomes claros e descritivos
- [ ] Complexidade reduzida (máx. 3-4 níveis de aninhamento)
- [ ] Constantes extraídas
- [ ] Tratamento de erros consistente
- [ ] Testes unitários cobrindo as mudanças
- [ ] Documentação atualizada
- [ ] Performance não comprometida
- [ ] Código revisado por pares

# Dicas Finais

- **Refatore incrementalmente:** Não tente refatorar todo o código de uma vez
- **Tenha testes:** Sempre tenha testes antes de refatorar
- **Meça o impacto:** Use ferramentas para medir complexidade e cobertura
- **Documente decisões:** Explique o "porquê" das mudanças importantes
