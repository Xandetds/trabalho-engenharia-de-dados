# Equipe

<style>
.team-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
}

.team-card {
  background: var(--md-default-bg-color);
  border: 1px solid var(--md-default-fg-color--lightest);
  border-radius: 12px;
  padding: 1.5rem 1rem;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0,0,0,.08);
  transition: box-shadow .2s, transform .2s;
}

.team-card:hover {
  box-shadow: 0 6px 20px rgba(0,0,0,.15);
  transform: translateY(-3px);
}

.team-card img {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 1rem;
  border: 3px solid var(--md-primary-fg-color);
}

.team-card h3 {
  margin: 0 0 .4rem;
  font-size: .95rem;
  font-weight: 700;
}

.team-card p {
  margin: 0;
  font-size: .82rem;
  color: var(--md-default-fg-color--light);
}
</style>

<div class="team-grid">

  <div class="team-card">
    <img src="../../assets/team/roger.jpeg" alt="Roger Balcevicz">
    <h3>Roger Balcevicz</h3>
    <p>Desenvolvedor JR</p>
  </div>

  <div class="team-card">
    <img src="../../assets/team/murilo.jpeg" alt="Murilo Salvan">
    <h3>Murilo Salvan</h3>
    <p>Manutenção Eletrônica</p>
  </div>

  <div class="team-card">
    <img src="../../assets/team/luis.jpeg" alt="Luis Filipe Damiani Colombo">
    <h3>Luis Filipe Damiani Colombo</h3>
    <p>Estudante</p>
  </div>

  <div class="team-card">
    <img src="../../assets/team/joao.jpeg" alt="João Miguel Fortunato Rita">
    <h3>João Miguel Fortunato Rita</h3>
    <p>Desenvolvedor JR</p>
  </div>

  <div class="team-card">
    <img src="../assets/team/gianluca.jpeg" alt="Gianluca Andrade Silvestre">
    <h3>Gianluca Andrade Silvestre</h3>
    <p>Desenvolvedor Pleno</p>
  </div>

  <div class="team-card">
    <img src="../assets/team/bruno.jpeg" alt="Bruno Monteiro Bonifacio">
    <h3>Bruno Monteiro Bonifacio</h3>
    <p>Desenvolvedor JR</p>
  </div>

  <div class="team-card">
    <img src="../assets/team/gustavo.jpeg" alt="Gustavo de Freitas Cardoso">
    <h3>Gustavo de Freitas Cardoso</h3>
    <p>Produção de Persianas</p>
  </div>

  <div class="team-card">
    <img src="../assets/team/alexandre.jpeg" alt="Alexandre Tibes da Silva">
    <h3>Alexandre Tibes da Silva</h3>
    <p>Suporte e Implantação Betha</p>
  </div>

</div>
