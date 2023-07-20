import ROOT as r


def set_batch(is_batch: bool) -> None:
    """
    gROOT->SetBatch(bool)のエイリアス
    """
    return r.gROOT.SetBatch(is_batch)


def set_opt_stat(show_stat: bool) -> None:
    """
    gStyle->SetOptStat(bool)のエイリアス
    """
    return r.gStyle.SetOptStat(show_stat)
