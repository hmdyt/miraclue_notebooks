import ROOT as r
import uuid
from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple

CVVAR_ROOTFILE = "cvvar.root"


class CvvarReader:
    tree: r.TTree
    tfile: r.TFile
    canvas: r.TCanvas

    def __init__(self, cvvar_path=CVVAR_ROOTFILE) -> None:
        self.open_cvvar(cvvar_path)

    def open_cvvar(self, cvvar_path=CVVAR_ROOTFILE) -> None:
        """
        カレントディレクトリのcvvar.rootを開く
        """
        self.tfile = r.TFile.Open(cvvar_path)
        self.tree = self.tfile.cvvar_tree

    def save(self, object: r.TObject, opt: str, save_as: str, logz=False) -> str:
        """
        objectをcanvasにdrawして保存する\n
        ex) `reader.save(hist, '', 'hist.png')`
        """
        self.canvas = r.TCanvas()
        object.Draw(opt)
        if logz:
            r.gPad.SetLogz()

        self.canvas.SaveAs(save_as)

    def hist(self, branch: str, hist_arguments: str, cut_contidion='') -> None:
        """
        あるブランチのヒストグラムを作成する\n

        ex) ene_lの0-1000を100binでdraw\n
        `reader.hist('ene_l', '100, 0, 1000')`\n

        ex) enel vs lentghの2d hist (0-50keV, 0-5cm) \n
        `reader.hist('length:ene_l', '100, 0, 50, 100, 0, 5', cut_condition='length < 5')`\n
        """
        id_ = uuid.uuid1()

        hist_name = f'hist_{id_}'
        self.tree.Draw(f'{branch}>>{hist_name}({hist_arguments})', cut_contidion)
        hist = r.gROOT.FindObject(hist_name)

        return hist.Clone()


@dataclass(frozen=True)
class Energy:
    """kev"""
    arr: List[float]


@dataclass(frozen=True)
class Length:
    """cm"""
    arr: List[float]


class SrimData:
    """
    中性子と任意の原子核の反跳の energy length データを返す\n
    (1気圧 Ar C2H6 = 9:1)
    """
    __hydrogen = Path("/home/hamada/analysis/NAP/SRIMdata/SRIM_H_in_760torr_ArC2H6.dat")
    __argon = Path("/home/hamada/analysis/NAP/SRIMdata/SRIM_Ar_in_760torr_ArC2H6.dat")

    @staticmethod
    def read(p: Path) -> Tuple[Energy, Length]:
        energy_list: List[float] = []
        length_list: List[float] = []
        with p.open() as f:
            for l in f.readlines():
                energy_kev, length_mm = map(float, l.split())
                length_list.append(length_mm / 10)  # mm -> cm
                energy_list.append(energy_kev)
        return Energy(energy_list), Length(length_list)

    @classmethod
    def hydrogen(cls) -> Tuple[Energy, Length]:
        return cls.read(cls.__hydrogen)

    @classmethod
    def argon(cls) -> Tuple[Energy, Length]:
        return cls.read(cls.__argon)
