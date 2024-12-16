package web.T4.data;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;

@Entity
public class Archivo {
  @Id
  private Integer id;

  private String ruta_archivo;

  @ManyToOne
  @JoinColumn(name = "dispositivo_id")
  private Dispositivo dispositivo;

  public Integer getId() {
    return id;
  }

  public String getRuta_archivo() {
    return ruta_archivo;
  }

  public Dispositivo getDispositivo() {
    return dispositivo;
  }
}
